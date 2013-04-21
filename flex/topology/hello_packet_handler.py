# encoding: utf-8
'''
Created on 2013-3-30

@author: kfirst
'''

from flex.core import core
from flex.base.handler import PacketHandler
from flex.base.event import NeighborControllerUpEvent
from flex.model.packet import HelloPacketContent, Packet
from flex.topology.topology import Topology

logger = core.get_logger()

class HelloPacketHandler(PacketHandler):
    '''
    维护邻居信息的工作原理是：
    当Controller1的topology模块启动起来后，将向其所有的邻居发送Hello报文；
    当Controller2收到Hello报文时，它就认为Controller1 Up了，
    并产生NeighborControllerUp事件，然后回复一个response Hello报文；
    当Controller1收到response Hello报文时，它就认为Controller2 Up了，
    并产生NeighborControllerUp事件。
    '''

    PROVIDER = Topology.PROVIDER
    PEER = Topology.PEER
    CUSTOMER = Topology.CUSTOMER

    def __init__(self, myself, relation_of_neighbor, neighbors_with_relation):
        self._myself = myself
        self._relation_of_neighbor = relation_of_neighbor
        self._neighbors_with_relation = neighbors_with_relation
        hello_packet_content = HelloPacketContent(self._myself)
        self._packet = Packet(Packet.HELLO, hello_packet_content)
        # send hello packet
        hello_packet = self._make_hello_packet()
        for neighbor in self._relation_of_neighbor:
            self._send_packet(hello_packet, neighbor)

    def get_neighbor_relation(self, controller):
        return self._relation_of_neighbor[controller]

    def get_neighbors(self):
        return set(self._relation_of_neighbor.keys())

    def get_peers(self):
        return set(self._neighbors_with_relation[self.PEER])

    def get_providers(self):
        return set(self._neighbors_with_relation[self.PROVIDER])

    def get_customers(self):
        return set(self._neighbors_with_relation[self.CUSTOMER])

    def handle_packet(self, packet):
        logger.debug('Hello packet received')

        up_controller = packet.content.controller
        try:
            relation = self._relation_of_neighbor[up_controller]
        except KeyError:
            logger.warning('There is no neighbor ' + str(up_controller))
            return
        if not packet.content.response:
            hello_packet = self._make_hello_packet(True)
            self._send_packet(hello_packet, up_controller)

        core.event.happen(NeighborControllerUpEvent(up_controller, relation))

    def _make_hello_packet(self, response = False):
        self._packet.content.response = response
        return self._packet

    def _send_packet(self, packet, dst):
        core.forwarding.forward(packet, dst)
