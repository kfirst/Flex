'''
Created on 2013-3-30

@author: kfirst
'''

from flex.core import core
from flex.base.handler import PacketHandler
from flex.base.event import NeighborControllerUpEvent
from flex.model.packet import Packet, PacketHeader, HelloPacketContent, TopologyPacketContent

logger = core.get_logger()

class HelloPacketHandler(PacketHandler):

    def __init__(self, topology):
        self._topo = topology

        # send hello packet
        hello_packet_content = HelloPacketContent(self._controllers[self._my_id])
        hello_packet = Packet(PacketHeader.HELLO, hello_packet_content)
        for cid in self._relation_of_neighbor:
            core.network.send(self._controllers[cid], hello_packet)

    def __getattr__(self, name):
        return getattr(self._topo, name)

    def handle(self, packet):
        logger.debug('Hello packet received')
        self._controllers[packet.content.controller.get_id()].up()
        if not packet.content.if_response:
            hello_packet_content = HelloPacketContent(self._controllers[self._my_id])
            hello_packet_content.if_response = True
            hello_packet = Packet(PacketHeader.HELLO, hello_packet_content)
            core.network.send(packet.content.controller, hello_packet)

        topo_packet_content = TopologyPacketContent(self._controllers[self._my_id], self._switches.keys(), set())
        topo_packet = Packet(PacketHeader.TOPO, topo_packet_content)
        core.network.send(packet.content.controller, topo_packet)

        core.event.happen(NeighborControllerUpEvent(self._controllers[self._my_id]))
