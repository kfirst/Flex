'''
Created on 2013-4-6

@author: fzm
'''

from flex.core import core
from flex.base.module import Module
from flex.model.packet import Packet, RegisterConcersContent
from flex.control_packet_forwarding.control_from_switch_handler import Control_From_Switch_Handler
from flex.control_packet_forwarding.register_concerns_handler import RegisterConcernsHandler
from flex.control_packet_forwarding.control_from_api_handler import Control_From_Api_Handler
from flex.base.event import NeighborControllerUpEvent
from flex.base.handler import EventHandler
from flex.topology.topology import Topology

logger = core.get_logger()

class ControlPacketForwarding(Module):

    def __init__(self):
        self.self_controller = core.myself.get_self_controller()
        self.self_id = self.self_controller.get_id()
        self.type = core.myself.get_self_type()
        self.controller_concerns = {}
        self.concern_types = {}

    def start(self):
        forwarding = core.forwarding
        forwarding.register_handler(Packet.CONTROL_FROM_SWITCH, Control_From_Switch_Handler(self))
        forwarding.register_handler(Packet.REGISTER_CONCERN, RegisterConcernsHandler(self))
        forwarding.register_handler(Packet.CONTROL_FROM_API, Control_From_Api_Handler(self))

        controller_up_handler = ControllerUpHandler(self)
        core.event.register_handler(NeighborControllerUpEvent, controller_up_handler)


class ControllerUpHandler(EventHandler):

    def __init__(self, control_packet_forwarding):
        self.control_packet_forwarding = control_packet_forwarding

    def handle(self, event):
        relation = event.relation
        if relation != Topology.PROVIDER and self.concern_types:
            myself = self.control_packet_forwarding.self_controller
            concern_types = self.control_packet_forwarding.concern_types
            content = RegisterConcersContent(myself, concern_types)
            packet = Packet(Packet.REGISTER_CONCERN, content)
            core.forwarding.forward(packet, event.controller)
