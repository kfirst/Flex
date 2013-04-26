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

    CONNECTION_UP = 'ConnectionUp'
    CONNECTION_DOWN = 'ConnectionDown'
    PACKET_IN = 'PacketIn'

    ALL_SWITCHES = RegisterConcersContent.ALL_SWITCHES

    _message = {
        ControlPacketContent.CONNECTION_UP: ConnectionUpMessage,
        ControlPacketContent.CONNECTION_DOWN: ConnectionDownMessage,
        ControlPacketContent.PACKET_IN: PacketInMessage
    }

    def __init__(self, self_controller):
        self._myself = self_controller
        self._all_switches = None
        # {type: {switch: method}}
        self._handlers = {}

    def start(self):
        controllers_update = [(self._myself, set())]
        content = TopologyControllerPacketContent(self._myself, controllers_update, [])
        packet = Packet(Packet.TOPO_CONTROLLER, content)
        core.forwarding.forward(packet)
        core.forwarding.register_handler(Packet.LOCAL_TO_API, self)

    def handle_packet(self, packet):
        content = packet.content
        switch = content.src
        control_type = content.type
        logger.info('Local To Api [' + control_type + '] packet received')
        flag = False
        try:
            message = self._message[control_type](self, content)
        except KeyError:
            logger.warning('No message for ' + str(packet))
            return
        try:
            handlers = self._handlers[control_type][switch]
            for handler in handlers:
                handler(message)
        except KeyError:
            flag = True
        try:
            handlers = self._handlers[control_type][self.ALL_SWITCHES]
            for handler in handlers:
                handler(message)
        except KeyError:
            if flag:
                logger.warning('No handler for ' + str(packet))

    @property
    def all_switches(self):
        from flex.api.structures import AllSwitches
        if not self._all_switches:
            self._all_switches = AllSwitches(self)
        return self._all_switches

    def _add_hanlders(self, app, switches = RegisterConcersContent.ALL_SWITCHES):
        concern_types = {}
        for method_name in dir(app):
            method = getattr(app, method_name)
            if callable(method) and method_name.startswith("_handle_"):
                control_type = method_name[8:]
                self._add_method(method, control_type, switches)
                concern_types[control_type] = switches
        if concern_types:
            self._send_concern(concern_types)

    def _add_hanlder(self, method, control_type, switches = RegisterConcersContent.ALL_SWITCHES):
        self._add_method(method, control_type, switches)
        self._send_concern({control_type: switches})

    def _add_method(self, method, control_type, switches):
        try:
            handlers = self._handlers[control_type]
        except KeyError:
            handlers = {}
            self._handlers[control_type] = handlers
        if switches == RegisterConcersContent.ALL_SWITCHES:
            switches = [switches]
        for switch in switches:
            try:
                handlers[switch].add(method)
            except KeyError:
                handlers[switch] = set([method])

    def _send_concern(self, concern_types):
        content = RegisterConcersContent(self._myself, concern_types)
        packet = Packet(Packet.REGISTER_CONCERN, content)
        core.forwarding.forward(packet)
