'''
Created on 2013-4-22

@author: kfirst
'''

from flex.base.module import Module
from flex.core import core
from flex.model.packet import *
from flex.api.messages import *
from flex.base.handler import PacketHandler

logger = core.get_logger()

class Api(Module, PacketHandler):

    LOCAL_CONCERN = 'local_concern'
    GLOBAL_CONCERN = 'global_concern'

    def __init__(self, self_controller):
        self._myself = self_controller
        self._all_switches = None
        # {type: {switch: [method]}}
        self._local_handlers = {}
        # {type: [method]}
        self._global_handlers = {}

    def start(self):
        core.forwarding.register_handler(Packet.CONTROL_FROM_SWITCH, self)

    def handle_packet(self, packet):
        content = packet.content
        switch = content.src
        control_type = content.type
        logger.info('CONTROL_FROM_SWITCH [' + control_type + '] packet received')
        handlers = set()
        try:
            handlers.update(self._global_handlers[control_type])
        except KeyError:
            pass
        try:
            handlers = self._local_handlers[control_type][switch]
        except KeyError:
            pass
        for handler in handlers:
            handler(content)

    @property
    def all_switches(self):
        from flex.api.structures import AllSwitches
        if not self._all_switches:
            self._all_switches = AllSwitches(self)
        return self._all_switches

    def _add_hanlders(self, app, switches = None):
        concern_types = []
        for method_name in dir(app):
            method = getattr(app, method_name)
            if callable(method) and method_name.startswith("_handle_"):
                control_type = method_name[8:]
                self._add_method(method, control_type, switches)
                concern_types.append(control_type)
        if concern_types:
            self._add_concern(concern_types, switches)

    def _add_hanlder(self, method, control_type, switches = None):
        self._add_method(method, control_type, switches)
        self._add_concern([control_type], switches)

    def _add_method(self, method, control_type, switches):
        if switches is None:
            try:
                self._global_handlers[control_type].add(method)
            except KeyError:
                self._global_handlers[control_type] = set([method])
        else:
            try:
                handlers = self._local_handlers[control_type]
            except KeyError:
                handlers = {}
                self._handlers[control_type] = handlers
            for switch in switches:
                try:
                    handlers[switch].add(method)
                except KeyError:
                    handlers[switch] = set([method])

    def _add_concern(self, concern_types, switches):
        if switches is None:
            core.globalStorage.sadd_multi(
                    self._myself.get_id(),
                    concern_types,
                    self.GLOBAL_CONCERN)
        else:
            for switch in switches:
                core.globalStorage.sadd_multi(
                        self._myself.get_id(),
                        concern_types,
                        '%s:%s' % (self.LOCAL_CONCERN, switch.get_id()))
