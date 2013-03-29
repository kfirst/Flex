'''
Created on 2013-3-19

@author: fzm
'''

from flex.model.device import Controller
from flex.model.packet import PacketHeader, Packet, TopologyPacketContent
from flex.core import core
from flex.base.module import module
from flex.base.exception import ControllerNotFound, SwitchNotFound


class TopoHandler(module):

    def __init__(self):
        self._controller_id = None

        self._controller_controllers = {}
        self._controller_nexthop = {}
        self._controller_neighbors = {}  # c->r
        self._controller_relations = {}  # r->c

        self._controller_switch = {}
        self._handlers = {
                          "peer": self._handle_peer,
                          "customer": self._handle_customer
                          }

    def start(self):
        core.network.register_handler(PacketHeader().type, self)

    def _handler_peer(self, packet):
        cid_src = packet.content.controller.get_id()
        for sid in packet.content.switches_added:
            if self._controller_switch.has_key(sid):
                self._controller_switch[sid].append(cid_src)
            else:
                self._controller_switch[sid] = []
                self._controller_switch[sid].append(cid_src)
        for sid in packet.content.switches_removed:
            self._controller_switch[sid].remove(cid_src)
    def _handler_customer(self, packet):
        cid_src = packet.content.controller.get_id()
        for sid in packet.content.switches_added:
            if self._controller_switch.has_key(sid):
                self._controller_switch[sid].insert(0, cid_src)
            else:
                self._controller_switch[sid] = []
                self._controller_switch[sid].append(cid_src)
        for sid in packet.content.switches_removed:
            self._controller_switch[sid].remove(cid_src)
        # network send packet
        packet.content.controller = self._controller_controllers[cid_src]
        packet.header.path.append(self._controller_controllers[cid_src])

        for cid in self._controller_relations['provider']:
            packet.header.dst = self._controller_controllers[cid]
            core.network.send(self._controller_controllers[cid], packet)
        for cid in self._controller_relations['peer']:
            packet.header.dst = self._controller_controllers[cid]
            core.network.send(self._controller_controllers[cid], packet)

    def handle(self, packet):
        cid = packet.content.controller.get_id()
        if self._controller_neighbors[cid] == 'peer':
            self.handle['peer'](packet)

        elif self._controller_neighbors[cid] == 'customer':
            self.handle['customer'](packet)

    def next_hop_of_controller(self, controller):
        try:
            return self._controller_controllers[self._controller_nexthop[controller.get_id()]]
        except KeyError:
            raise ControllerNotFound('The nexthop of ' + controller + ' is not found!')

    def next_hop_of_switch(self, switch):
        try:
            return self._controller_controllers[self._controller_switch[switch.get_id()][0]]
        except KeyError:
            raise SwitchNotFound('The nexthop of ' + switch + ' is not found!')

