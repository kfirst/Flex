'''
Created on 2013-4-6

@author: fzm
'''
from flex.core import core
from flex.base.handler import PacketHandler

logger = core.get_logger()

class Register_Concerns_Handler(PacketHandler):
    def __init__(self, control_packet_forwarding):
        self._control = control_packet_forwarding

    def __getattr__(self, name):
        return getattr(self._control, name)

    def handle(self, packet):
        controller = packet.header.controller
        types = packet.header.type
        for ttype in types:
            try:
                self.type_controller[ttype].add(controller)
            except KeyError:
                self.type_controller[ttype] = set([controller])

        self.send_packet_to_neighbors(packet)

    def send_packet_to_neighbors(self, packet):
        peer_controllers = core.topology.get_peer_controller()
        customer_controllers = core.topology.get_customer_controller()

        packet.content.controller = self.self_controller
        # packet.content.type = self.type_controller.keys()

        for controller in peer_controllers:
            core.network.send(controller, packet)

        for controller in customer_controllers:
            core.network.send(controller, packet)
