'''
Created on 2013-3-19

@author: fzm
'''

from flex.core import core
from flex.base.module import Module
from flex.base.exception import SwitchNotFoundException
from flex.topology.topo_packet_handler import TopoPacketHandler
from flex.topology.hello_packet_handler import HelloPacketHandler
from flex.model.packet import Packet

logger = core.get_logger()

class Topology(Module):

    def __init__(self):
        self._myself = None
        self._controllers = {}
        self._relation_of_neighbor = {}
        self._neighbors_with_relation = {}
        self._controllers_of_switch = {}
        self._switches = {}

    def start(self):
        forwarding = core.forwarding
        forwarding.register_handler(Packet.TOPO, TopoPacketHandler(self))
        forwarding.register_handler(Packet.HELLO, HelloPacketHandler(self))

    def next_hop_of_switch(self, switch):
        try:
            for cid in self._controllers_of_switch[switch.get_id()]:
                controller = self._controllers[cid]
                if controller.is_up():
                    return controller
        except KeyError:
            raise SwitchNotFoundException(str(switch) + ' is not found!')
        else:
            raise SwitchNotFoundException('The nexthop of ' + str(switch) + ' is not found!')

    def get_neighbor_relation(self, controller):
        return self._relation_of_neighbor[controller.get_id()]

    def get_neighbors(self):
        return self._filter_controller(self._relation_of_neighbor.keys())

    def get_peers(self):
        return self._filter_controller(self._neighbors_with_relation['peer'])

    def get_providers(self):
        return self._filter_controller(self._neighbors_with_relation['provider'])

    def get_customers(self):
        return self._filter_controller(self._neighbors_with_relation['customer'])

    def _filter_controller(self, controller_ids):
        controller_set = set()
        for cid in controller_ids:
            controller = self._controllers[cid]
            if controller.is_up():
                controller_set.add(controller)
        return controller_set
