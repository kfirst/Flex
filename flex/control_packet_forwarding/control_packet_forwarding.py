'''
Created on 2013-4-6

@author: fzm
'''

from flex.core import core
from flex.base.module import Module
from flex.model.packet import Packet, RegisterConcersContent
from flex.control_packet_forwarding.control_from_switch_handler import ControlFromSwitchHandler
from flex.control_packet_forwarding.register_concerns_handler import RegisterConcernsHandler
from flex.control_packet_forwarding.control_from_api_handler import ControlFromApiHandler
from flex.base.event import NeighborControllerUpEvent
from flex.base.handler import EventHandler
from flex.topology.topology import Topology

logger = core.get_logger()

class ControlPacketForwarding(Module):

    def __init__(self, self_controller, algorithms):
        self.self_controller = self_controller
        self.controller_concerns = {}
        self.algorithms = algorithms

    def start(self):
        cfs = ControlFromSwitchHandler(self.self_controller, self.controller_concerns, self.algorithms)
        cfa = ControlFromApiHandler(self.self_controller)
        rc = RegisterConcernsHandler(self.controller_concerns)

        forwarding = core.forwarding
        forwarding.register_handler(Packet.CONTROL_FROM_SWITCH, cfs)
        forwarding.register_handler(Packet.CONTROL_FROM_API, cfa)
        forwarding.register_handler(Packet.REGISTER_CONCERN, rc)

        cuh = ControllerUpHandler(self.controller_concerns)
        core.event.register_handler(NeighborControllerUpEvent, cuh)


class ControllerUpHandler(EventHandler):

    def __init__(self, controller_concerns):
        self._controller_concerns = controller_concerns

    def handle_event(self, event):
        relation = event.relation
        if relation == Topology.PEER or relation == Topology.CUSTOMER:
            for controller, types in self._controller_concerns.items():
                if types:
                    content = RegisterConcersContent(controller, types)
                    packet = Packet(Packet.REGISTER_CONCERN, content)
                    core.forwarding.forward(packet, event.controller)
