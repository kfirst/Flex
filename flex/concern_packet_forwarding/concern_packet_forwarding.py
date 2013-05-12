'''
Created on 2013-4-6

@author: fzm
'''

from flex.core import core
from flex.base.module import Module
from flex.model.packet import Packet, RegisterConcersContent
from flex.base.event import NeighborControllerUpEvent
from flex.base.handler import EventHandler
from flex.topology.topology import Topology
from flex.concern_packet_forwarding.register_concerns_handler import RegisterConcernsHandler

logger = core.get_logger()

class ConcernPacketForwarding(Module):

    def __init__(self, self_controller, algorithms):
        self.self_controller = self_controller
        self.controller_concerns = {}
        self.algorithms = algorithms

    def start(self):
        rc = RegisterConcernsHandler(self.controller_concerns)

        forwarding = core.forwarding
        forwarding.register_handler(Packet.REGISTER_CONCERN, rc)

        cuh = ControllerUpHandler(self.self_controller, self.controller_concerns)
        core.event.register_handler(NeighborControllerUpEvent, cuh)


class ControllerUpHandler(EventHandler):

    def __init__(self, self_controller, controller_concerns):
        self.self_controller = self_controller
        self._controller_concerns = controller_concerns

    def handle_event(self, event):
        relation = event.relation
        if relation == Topology.PEER or relation == Topology.CUSTOMER:
            for controller, types in self._controller_concerns.items():
                if types:
                    content = RegisterConcersContent(controller, types)
                    packet = Packet(Packet.REGISTER_CONCERN, content)
                    packet.src = self.self_controller
                    packet.dst = event.controller
                    core.forwarding.forward(packet)
