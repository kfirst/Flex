# encoding: utf-8
'''
Created on 2013-3-30

@author: kfirst
'''

from flex.core import core
from flex.base.handler import PacketHandler, EventHandler
from flex.model.packet import TopologySwitchPacketContent, Packet
from flex.topology.topology import Topology
from flex.topology.topology_packet_handler import TopologyPacketHandler

logger = core.get_logger()

class SwitchPacketHandler(TopologyPacketHandler, PacketHandler, EventHandler):
    '''
    维护邻居可达的Switch信息的工作原理是：
    当Controller的一个peer或provider Controller Up时，
    Controller会将其可达的Switch和与Switch的距离发送给Up的Controller；
    当一个Controller收到Switch信息后，若自己没有该Switch的信息或者收到的信息中Switch距离更短，
    则更新自己的信息，然后检查发送者的身份，若为peer或customer，
    则将自己信息中更新的Switch（注意不是收到报文中的全部Switch），
    发给除发送者外的已经up的peer或provider。
    '''

    PROVIDER = Topology.PROVIDER
    PEER = Topology.PEER
    CUSTOMER = Topology.CUSTOMER

    def __init__(self, myself, relation_of_neighbor, neighbors_with_relation):
        super(SwitchPacketHandler, self).__init__(myself, relation_of_neighbor, neighbors_with_relation)

    def handle_event(self, event):
        relation = event.relation
        if relation == self.PEER or relation == self.PROVIDER:
            dst = event.controller
            update = []
            for switch, path in self._nexthop_of_device.items():
                update.append((switch, path[1]))
            if update:
                content = TopologySwitchPacketContent(self._myself, update, [])
                packet = Packet(Packet.TOPO_SWITCH, content)
                self._send_packet(packet, dst)

    def handle_packet(self, packet):
        logger.debug('Topo packet received')

        controller = packet.content.controller
        try:
            relation = self._relation_of_neighbor[controller]
        except KeyError:
            if controller == self._myself:
                relation = self.CUSTOMER
            else:
                logger.warning('There is no neighbor ' + controller)
                return
        if relation == self.PEER or relation == self.CUSTOMER:
            self._handle_packet(packet, controller)
        else:
            logger.warning('Provider ' + controller + 'should NOT send ' + packet)

    def _handle_packet(self, packet, src):
        remove, update = self._remove(src, packet.content.remove)
        update += self._update(src, packet.content.update)
        # network send packet
        if update or remove:
            content = TopologySwitchPacketContent(self._myself, update, remove)
            packet = Packet(Packet.TOPO_SWITCH, content)
            for c in self._neighbors_with_relation[self.PROVIDER]:
                if c != src:
                    self._send_packet(packet, c)
            for c in self._neighbors_with_relation[self.PEER]:
                if c != src:
                    self._send_packet(packet, c)
