'''
Created on 2013-3-30

@author: kfirst
'''

from flex.core import core
from flex.base.handler import PacketHandler
from flex.base.event import NeighborControllerUpEvent
from flex.model.packet import Packet, HelloPacketContent, TopologyPacketContent
from flex.topology.topology import Topology

logger = core.get_logger()

class HelloPacketHandler(PacketHandler):

    def __init__(self, topology):
        self._topo = topology

        # send hello packet
        hello_packet_content = HelloPacketContent(self._myself)
        hello_packet = Packet(Packet.HELLO, hello_packet_content)
        for cid in self._relation_of_neighbor:
            self._send_packet(self._controllers[cid], hello_packet)

    def __getattr__(self, name):
        return getattr(self._topo, name)

    def handle(self, packet):
        logger.debug('Hello packet received')

        controller = packet.content.controller
        if self._relation_of_neighbor(controller) != Topology.CUSTOMER:
            switch_added = self._switches.values()
            if switch_added:
                topo_packet_content = TopologyPacketContent(self._myself, switch_added, set())
                topo_packet = Packet(Packet.TOPO, topo_packet_content)
                self._send_packet(controller, topo_packet)

        if not packet.content.response:
            hello_packet_content = HelloPacketContent(self._myself, True)
            hello_packet = Packet(Packet.HELLO, hello_packet_content)
            self._send_packet(packet.content.controller, hello_packet)

        up_controller_id = packet.content.controller.get_id()
        up_controller = self._controllers[up_controller_id]
        up_controller.up()
        core.event.happen(NeighborControllerUpEvent(up_controller, self._relation_of_neighbor[up_controller_id]))

    def _send_packet(self, dst, packet):
        core.forwarding.forward(packet, dst)
