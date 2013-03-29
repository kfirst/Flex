'''
Created on 2013-3-26

@author: fzm
'''
from flex.model.device import Controller

class TopologyParser(object):

    def __init__(self, config):
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
        topo = {}
        for cid in controller_infos:
            topo[cid] = controller_infos[cid]['neighbors']
        return topo

    def _parse_nexthop(self, topo):
        nexthops = {}
        controller_id = self.my_id

        controller_step = {}
        # topo_of_controller = {}
        for cid in topo:
            controller_step[cid] = 0

        controller_step[controller_id] = 1;
        step = 1
        controller_set = topo[controller_id]
        # 搜索
        while True:
            step = step + 1
            controller_step_temp = set()
            for cid in controller_set:
                controller_step[cid] = step
            if len(controller_set) == 0:
                break
            for cid in controller_set:
                for neighbor_cid in topo[cid]:
                    if controller_step[neighbor_cid] == 0:
                        controller_step_temp.add(neighbor_cid)
            controller_set = controller_step_temp
        # 回溯
        for cid in topo:
            if cid != controller_id:
                controller_temp = cid
                while True:
                    if controller_step[controller_temp] == 2:
                        nexthops[cid] = controller_temp
                        break
                    elif controller_step[controller_temp] == 0:
                        break
                    for neighbor_cid in topo[controller_temp]:
                        if controller_step[neighbor_cid] == controller_step[controller_temp] - 1:
                            controller_temp = neighbor_cid;
                            break

        return nexthops

    def _parse_neighbors(self, topo):
        neighbor = {}
        neighbor_controller_infos = topo[self.my_id]
        for cid in neighbor_controller_infos:
            neighbor[cid] = neighbor_controller_infos[cid]
        return neighbor

    def _parse_relations(self, neighbors):
        relation = {}
        peer = set()
        customer = set()
        provider = set()
        for cid in neighbors:
            if neighbors[cid] == 'peer':
                peer.add(cid)
            elif neighbors[cid] == 'customer':
                customer.add(cid)
            elif neighbors[cid] == 'provider':
                provider.add(cid)
        relation['peer'] = peer
        relation['customer'] = customer
        relation['provider'] = provider
        return relation





