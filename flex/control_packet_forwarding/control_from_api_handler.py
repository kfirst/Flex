'''
Created on 2013-4-9

@author: fzm
'''
from flex.core import core
from flex.base.handler import PacketHandler
from flex.model.packet import  Packet

logger = core.get_logger()

class Control_From_Api_Handler(PacketHandler):
    def __init__(self, control_packet_forwarding):
        self._forwarding = control_packet_forwarding

    def __getattr__(self, name):
        return getattr(self._forwarding, name)

    def handle(self, packet):
        target_controller = core.topology.next_hop_of_switch(packet.content.dst)

        if target_controller.get_id() != self.self_id:
            core.network.send(target_controller, packet)
        else:
            packet.type = Packet.LOCAL_TO_POX
            core.network.send(target_controller, packet)


