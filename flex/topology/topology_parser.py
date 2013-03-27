'''
Created on 2013-3-26

@author: kfirst
'''
from flex.model.device import Controller

class TopologyParser(object):

    def parse(self, config):
        self.my_id = config.get('topology.my_id')
        controller_infos = config.get('topology.controllers')
        self.controllers = self._parse_controllers(controller_infos)
        topo = self._parse_topo(controller_infos)
        self.nexthop = self._parse_nexthop(topo)
        self.neighbors = self._parse_neighbors(topo)
        self.relations = self._parse_relations(self.neighbors)

    def _parse_controllers(self, controller_infos):
        controllers = {}
        for cid in controller_infos:
            address = tuple(controller_infos[cid]['address'])
            controller = Controller(cid, address)
            controllers[cid] = controller
        return controllers

    def _parse_topo(self, controller_infos):
        # TODO
        pass

    def _parse_nexthop(self, topo):
        # TODO
        pass

    def _parse_neighbors(self, topo):
        # TODO
        pass

    def _parse_relations(self, neighbors):
        # TODO
        pass
