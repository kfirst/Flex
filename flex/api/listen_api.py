'''
Created on 2013-5-15

@author: kfirst
'''

from flex.core import core
from flex.base.module import Module
from flex.model.packet import Packet, SwitchPacketContent
from flex.controller_adaptor.controller_adaptor import ControllerAdaptor
from flex.base.handler import PacketHandler

logger = core.get_logger()


class ListenApi(Module, PacketHandler):

    LOCAL_CONCERN = ControllerAdaptor.LOCAL_CONCERN
    GLOBAL_CONCERN = ControllerAdaptor.GLOBAL_CONCERN
    GLOBAL_CONCERN_CONTROLLERS = ControllerAdaptor.GLOBAL_CONCERN_CONTROLLERS

    CONCERN_TYPE = {
            'PacketIn': SwitchPacketContent.PACKET_IN,
            'ConnectionUp': SwitchPacketContent.CONNECTION_UP,
            'ConnectionDown': SwitchPacketContent.CONNECTION_DOWN,
    }

    def __init__(self):
        self._myself = core.myself.get_self_controller()
        # {type: {switch: [method]}}
        self._local_handlers = {}
        # {type: [method]}
        self._global_handlers = {}

    def start(self):
        core.forwarding.register_handler(Packet.CONTROL_FROM_SWITCH, self)

    def handle_packet(self, packet):
        content = packet.content
        control_type = content.type
        try:
            handlers = self._global_handlers[control_type]
            for handler in handlers:
                handler(content)
        except KeyError:
            pass
        try:
            switch = content.src
            handlers = self._local_handlers[control_type][switch]
            for handler in handlers:
                handler(content)
        except KeyError:
            pass

    def add_listeners(self, app, switch = None):
        concern_types = []
        for method_name in dir(app):
            method = getattr(app, method_name)
            if callable(method) and method_name.startswith("_handle_"):
                control_type = self.CONCERN_TYPE[method_name[8:]]
                self._add_method(method, control_type, switch)
                concern_types.append(control_type)
        if concern_types:
            self._add_concern(concern_types, switch)

    def add_listener(self, method, control_type, switch = None):
        control_type = self.CONCERN_TYPE[control_type]
        self._add_method(method, control_type, switch)
        self._add_concern([control_type], switch)

    def _add_method(self, method, control_type, switch):
        if switch is None:
            try:
                self._global_handlers[control_type].add(method)
            except KeyError:
                self._global_handlers[control_type] = set([method])
        else:
            try:
                handlers = self._local_handlers[control_type]
            except KeyError:
                handlers = {}
                self._local_handlers[control_type] = handlers
            try:
                handlers[switch].add(method)
            except KeyError:
                handlers[switch] = set([method])

    def _add_concern(self, concern_types, switch):
        if switch is None:
            core.globalStorage.sadd_multi(
                    self._myself.get_id(),
                    concern_types,
                    self.GLOBAL_CONCERN)
            core.globalStorage.sadd(
                    self.GLOBAL_CONCERN_CONTROLLERS,
                    self._myself.get_id(),
                    self.GLOBAL_CONCERN_CONTROLLERS)
        else:
            core.globalStorage.sadd_multi(
                    self._myself.get_id(),
                    concern_types,
                    '%s:%s' % (self.LOCAL_CONCERN, switch.get_id()))
