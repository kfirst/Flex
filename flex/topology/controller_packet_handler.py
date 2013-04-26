# encoding: utf-8
'''
Created on 2013-3-30

@author: kfirst
'''

from flex.core import core
from flex.base.handler import PacketHandler, EventHandler
from flex.model.packet import TopologyControllerPacketContent, Packet
from flex.topology.topology import Topology
from flex.topology.topology_packet_handler import TopologyPacketHandler

logger = core.get_logger()

class ControllerPacketHandler(TopologyPacketHandler, PacketHandler, EventHandler):
    '''
    维护邻居可达的Controller信息的工作原理是：
    当Controller的一个peer或customer Controller Up时，
    Controller会将其可达的Controller和与其的距离发送给Up的Controller；
    当一个Controller收到信息后，若自己没有该Controller的信息或者收到的信息中距离更短，
    则更新自己的信息，然后检查发送者的身份，若为peer或provider，
    则将自己信息中更新的Controller（注意不是收到报文中的全部Switch），
    发给除发送者外的已经up的peer或customer。
    '''

    PROVIDER = Topology.PROVIDER
    PEER = Topology.PEER
    CUSTOMER = Topology.CUSTOMER

    def __init__(self, myself, hello):
        super(ControllerPacketHandler, self).__init__(myself)
        self._myself = myself
        self._hello = hello

    def handle_event(self, event):
        relation = event.relation
        if relation == self.PEER or relation == self.CUSTOMER:
            dst = event.controller
            update = []
            for controller, nexthop in self._nexthop_of_device.items():
                update.append((controller, nexthop[1]))
            if update:
                content = TopologyControllerPacketContent(self._myself, update, [])
                packet = Packet(Packet.TOPO_CONTROLLER, content)
                self._send_packet(packet, dst)

    def handle_packet(self, packet):
        logger.info('Controller Topo packet received')

        src = packet.content.controller
        try:
            relation = self._hello.get_neighbor_relation(src)
        except KeyError:
            if src == self._myself:
                relation = self.PROVIDER
            else:
                logger.warning('There is no neighbor ' + src)
                return
        if relation == self.PEER or relation == self.PROVIDER:
            self._handle_packet(packet, src)
        else:
            logger.warning(str(relation) + ' ' + str(src) + ' should NOT send ' + str(packet))

    def _handle_packet(self, packet, src):
        remove, update = self._remove(src, packet.content.remove)
        update += self._update(src, packet.content.update)
        # network send packet
        if update or remove:
            content = TopologyControllerPacketContent(self._myself, update, remove)
            packet = Packet(Packet.TOPO_CONTROLLER, content)
            for customer in self._hello.get_customers():
                if customer != src:
                    self._send_packet(packet, customer)
            for peer in self._hello.get_peers():
                if peer != src:
                    self._send_packet(packet, peer)
