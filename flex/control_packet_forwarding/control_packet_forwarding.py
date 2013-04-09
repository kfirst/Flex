'''
Created on 2013-4-6

@author: fzm
'''

from flex.core import core
from flex.base.module import Module
from flex.model.packet import Packet, RegisterConcersContent
from flex.control_packet_forwarding.control_from_switch_handler import Control_From_Switch_Handler
from flex.control_packet_forwarding.register_concerns_handler import Register_Concerns_Handler
from flex.base.event import NeighborControllerUpEvent

logger = core.get_logger()

class ControlPacketForwarding(Module):
    def __init__(self):
        self.self_controller = core.myself.get_self_controller()
        self.self_id = self.self_controller.get_id()
        self.type_module = {}
        self.type_controller = {}

    def start(self):
        network = core.network
        network.register_handler(Packet.CONTROL_FROM_SWITCH, Control_From_Switch_Handler(self))
        network.register_handler(Packet.REGISTER_CONCERN, Register_Concerns_Handler(self))

        control_up_handler = ControlUpRegisterConcernHandler(self)
        core.event.register_handler(NeighborControllerUpEvent, control_up_handler)

    def register(self, ttype, modules):
        try:
            self.type_controller[ttype].add(self.self_controller)
        except KeyError:
            self.type_controller[ttype] = set([self.self_controller])

        if ttype in self.type_module:
            self.type_module[ttype] &= modules
        else:
            self.type_module[ttype] = modules

class ControlUpRegisterConcernHandler(object):
    def __init__(self, control_packet_forwarding):
        self.types = control_packet_forwarding.type_controller.keys()

    def handle(self, event):
        self.controller = event.controller
        self.relation = event.relation

        content = RegisterConcersContent(self.controller, self.types)
        packet = Packet(Packet.REGISTER_CONCERN, content)
        if self.relation != 'provider':
            core.network.send(self.controller, packet)





