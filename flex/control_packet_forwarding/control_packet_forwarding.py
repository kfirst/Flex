'''
Created on 2013-4-6

@author: fzm
'''

from flex.core import core
from flex.base.module import Module
from flex.model.packet import Packet, RegisterConcersContent
from flex.control_packet_forwarding.control_from_switch_handler import Control_From_Switch_Handler
from flex.control_packet_forwarding.register_concerns_handler import Register_Concerns_Handler
from flex.control_packet_forwarding.control_from_api_handler import Control_From_Api_Handler
from flex.base.event import NeighborControllerUpEvent
from flex.base.handler import EventHandler

logger = core.get_logger()

class ControlPacketForwarding(Module):
    def __init__(self):
        self.self_controller = core.myself.get_self_controller()
        self.self_id = self.self_controller.get_id()
        self.type = core.myself.get_self_type()
        self.type_controller = {}

    def start(self):
        network = core.network
        network.register_handler(Packet.CONTROL_FROM_SWITCH, Control_From_Switch_Handler(self))
        network.register_handler(Packet.REGISTER_CONCERN, Register_Concerns_Handler(self))
        network.register_handler(Packet.CONTROL_FROM_API, Control_From_Api_Handler(self))

        control_up_handler = ControlUpRegisterConcernHandler(self)
        core.event.register_handler(NeighborControllerUpEvent, control_up_handler)

class ControlUpRegisterConcernHandler(EventHandler):
    def __init__(self, control_packet_forwarding):
        self.control_packet_forwarding = control_packet_forwarding

    def handle(self, event):
        self.controller = event.controller
        self.relation = event.relation

        concern_types = self.control_packet_forwarding.type_controller.keys()
        content = RegisterConcersContent(self.controller, concern_types)
        packet = Packet(Packet.REGISTER_CONCERN, content)
        if self.relation != 'provider' and concern_types:
            core.network.send(self.controller, packet)





