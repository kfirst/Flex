'''
Created on 2013-4-9

@author: fzm
'''
from flex.core import core
from flex.base.handler import PacketHandler
from flex.model.packet import  Packet

logger = core.get_logger()

class ControlFromApiHandler(PacketHandler):

    def __init__(self, self_controller):
        self._myself = self_controller

    def handle_packet(self, packet):
        logger.info('Control from api packet received')
        nexthop = core.topology.nexthop(packet.content.dst)
        if nexthop == self._myself:
            packet.type = Packet.LOCAL_TO_POX
            core.forwarding.forward(packet)
        else:
            core.forwarding.forward(packet, nexthop)
