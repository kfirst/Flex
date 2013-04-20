# encoding: utf-8
'''
Created on 2013-3-30

@author: kfirst
'''

from flex.core import core
from flex.base.handler import PacketHandler, EventHandler
from flex.model.packet import TopologySwitchPacketContent, Packet
from flex.topology.topology import Topology

logger = core.get_logger()

class SwitchPacketHandler(PacketHandler, EventHandler):
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
        self._myself = myself
        self._my_id = myself.get_id();
        self._relation_of_neighbor = relation_of_neighbor
        self._neighbors_with_relation = neighbors_with_relation
        # {switch: {controller: path}}
        self._controllers_of_switch = {}
        # {switch: (controller, path)}
        self._nexthop_of_switch = {}

    def _send_packet(self, packet, dst):
        core.forwarding.forward(packet, dst)

    def next_hop_of_switch(self, switch):
        return self._nexthop_of_switch[switch][0]

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

    def handle_event(self, event):
        relation = event.relation
        if relation == self.PEER or relation == self.PROVIDER:
            dst = event.controller
            update = []
            for switch, path in self._nexthop_of_switch.items():
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

    def _handle_packet(self, packet, controller):
        src = packet.content.controller.get_id()
        remove, update = self._remove(src, packet.content.remove)
        update += self._update(src, packet.content.update)
        # network send packet
        if update or remove:
            content = TopologySwitchPacketContent(self._myself, update, remove)
            packet = Packet(Packet.TOPO_SWITCH, content)
            for c in self._neighbors_with_relation[self.PROVIDER]:
                if c != controller:
                    self._send_packet(packet, c)
            for c in self._neighbors_with_relation[self.PEER]:
                if c != controller:
                    self._send_packet(packet, c)

    def _remove(self, src, switches):
        remove = []
        update = []
        for switch in switches:
            try:
                controllers = self._controllers_of_switch[switch]
                nexthop = self._nexthop_of_switch[switch]
                controllers.pop(src, None)
                if src == nexthop[0]:
                    remove.append(switch)
                    shortest = None
                    for controller in controllers.items():
                        if shortest == None or len(controller[1]) < len(shortest[1]):
                            shortest = controller
                    if shortest == None:
                        del self._nexthop_of_switch[switch]
                    else:
                        self._nexthop_of_switch[switch] = shortest
                        update.append((switch, shortest[1]))
            except KeyError:
                logger.warning(str(switch) + ' is not found!');
        return (remove, update)

    def _update(self, src, switches):
        update = []
        for switch, path in switches:
            if self._my_id in path:
                continue
            path.add(self._myself.get_id())
            try:
                controllers = self._controllers_of_switch[switch]
                nexthop = self._nexthop_of_switch[switch]
                if src in controllers:
                    if len(path) < len(controllers[src]):
                        controllers[src] = path
                else:
                    controllers[src] = path
                if len(path) < len(nexthop[1]):
                    nexthop[0] = src
                    nexthop[1] = path
                    update.append((switch, path))
            except KeyError:
                self._controllers_of_switch[switch] = {src: path}
                nexthop = [src, path]
                self._nexthop_of_switch[switch] = nexthop
                update.append((switch, path))
        return update
