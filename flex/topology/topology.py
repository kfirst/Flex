'''
Created on 2013-3-19

@author: fzm
'''

from flex.topology.find_hop_of_switch import FindHopOfSwitch
from flex.topology.find_hop_of_controller import FindHopOfController
from flex.model.device import Controller
from flex.model.packet import PacketHeader, Packet, TopologyPacketContent
from flex.core import core


class TopoHandler(object):

    def __init__(self):
        self._controller_id = None
        
        self._controller_controllers = {}
        self._controller_nexthop = {}
        self._controller_neighbors = {}#c->r
        self._controller_relations = {}#r->c
        
        self._controller_switch = {}

    def handle(self, packet):
        cid = packet.content.controller.get_id()
        a = set()
        for i in self._controller_switch:
            a.add(i)
        b = set()  
        if self._controller_neighbors[cid] == 'peer':
            for i in packet.content.switches_added:
                if self._controller_switch.has_key(i):
                    self._controller_switch[i].append(cid)
                else:
                    self._controller_switch[i] = []
                    self._controller_switch[i].append(cid)
            for i in packet.content.switches_removed:
                self._controller_switch[i].remove(cid)
            
        elif self._controller_neighbors[packet.content.controller.get_id()] == 'customer':
            for i in packet.content.switches_added:
                if self._controller_switch.has_key(i):
                    self._controller_switch[i].insert(0, cid)
                else:
                    self._controller_switch[i] = []
                    self._controller_switch[i].append(cid)
            for i in packet.content.switches_removed:
                self._controller_switch[i].remove(cid)
            for i in self._controller_switch:
                b.add(i)
            #packet
            packet.content.controller = self._controller_controllers[cid]
            packet.content.switches_added = b - a
            packet.content.switches_removed = a - b
            packet.header.path.append(self._controller_controllers[cid])
            
            for i in self._controller_relations['provider']:
                packet.header.dst = self._controller_controllers[i]
                core.network.send(self._controller_controllers[i], packet)
            for i in self._controller_relations['peer']:
                packet.header.dst = self._controller_controllers[i]
                core.network.send(self._controller_controllers[i], packet)
                 
    def next_hop_of_controller(self, controller):
        return self._controller_controllers[self._controller_nexthop[controller.get_id()]]

    def next_hop_of_switch(self, switch):
        return self._controller_controllers[self._controller_switch[switch.get_id()][0]]
