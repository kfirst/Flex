'''
Created on 2013-3-30

@author: kfirst
'''

from flex.core import core
from flex.base.handler import PacketHandler
from flex.base.event import NeighborControllerUpEvent
from flex.model.packet import Packet, HelloPacketContent, TopologyPacketContent

logger = core.get_logger()

class HelloPacketHandler(PacketHandler):

    def __init__(self, topology):
        self._topo = topology

        # send hello packet
        hello_packet_content = HelloPacketContent(self._controllers[self._my_id])
        hello_packet = Packet(Packet.HELLO, hello_packet_content)
        for cid in self._relation_of_neighbor:
            core.network.send(self._controllers[cid], hello_packet)

    def __getattr__(self, name):
        return getattr(self._topo, name)

    def handle(self, packet):
        logger.debug('Hello packet received')
        self._controllers[packet.content.controller.get_id()].up()
        if not packet.content.response:
            hello_packet_content = HelloPacketContent(self._controllers[self._my_id])
            hello_packet_content.response = True
            hello_packet = Packet(Packet.HELLO, hello_packet_content)
            core.network.send(packet.content.controller, hello_packet)

        switch_added = self._connection_fds.keys()
        if switch_added:
            topo_packet_content = TopologyPacketContent(self._controllers[self._my_id], switch_added, set())
            topo_packet = Packet(Packet.TOPO, topo_packet_content)
            core.network.send(packet.content.controller, topo_packet)

        up_controller = packet.content.controller
        core.event.happen(NeighborControllerUpEvent(up_controller, self._relation_of_neighbor[up_controller.get_id()]))
