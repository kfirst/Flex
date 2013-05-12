# encoding: utf-8
'''
Created on 2013-3-26

@author: fzm
'''

from flex.model.device import Controller
from flex.core import core
from flex.topology.topology import Topology

class NeighborParser(object):

    def __init__(self, config):
        self.myself = core.myself.get_self_controller()
        self.my_id = self.myself.get_id()
        controller_infos = config.get('topology.controllers')
        neighbor_info = controller_infos[self.my_id]['neighbors']
        del controller_infos[self.my_id]

        self.controllers = self._parse_controllers(controller_infos)
        self.controllers[self.myself.get_id()] = self.myself
        self.neighbors = self._parse_neighbors(neighbor_info)
        self.relations = self._parse_relations(neighbor_info)

    def _parse_controllers(self, controller_infos):
        controllers = {}
        for cid in controller_infos:
            controller = Controller(cid, controller_infos[cid]['address'])
            controllers[cid] = controller
        return controllers

    def _parse_neighbors(self, neighbor_info):
        neighbor = {}
        for cid in neighbor_info:
            neighbor[self.controllers[cid]] = neighbor_info[cid]
        return neighbor

    def _parse_relations(self, neighbor_info):
        relation = {}
        peer = set()
        customer = set()
        provider = set()
        for cid in neighbor_info:
            controller = self.controllers[cid]
            if neighbor_info[cid] == Topology.PEER:
                peer.add(controller)
            elif neighbor_info[cid] == Topology.CUSTOMER:
                customer.add(controller)
            elif neighbor_info[cid] == Topology.PROVIDER:
                provider.add(controller)
        relation[Topology.PEER] = peer
        relation[Topology.CUSTOMER] = customer
        relation[Topology.PROVIDER] = provider
        return relation
