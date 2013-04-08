'''
Created on 2013-3-19

@author: fzm
'''

from flex.model.packet import PacketHeader
from flex.core import core
from flex.base.module import Module
from flex.base.exception import ControllerNotFoundException, SwitchNotFoundException
from flex.topology.topo_packet_handler import TopoPacketHandler
from flex.topology.hello_packet_handler import HelloPacketHandler

logger = core.get_logger()

class Topology(Module):

    def __init__(self):
        self._my_id = None
        self._controllers = {}
        self._nexthop_of_controller = {}
        self._relation_of_neighbor = {}  # c->r
        self._neighbors_with_relation = {}  # r->c
        self._controllers_of_switch = {}
        self._switches = {}

    def start(self):
        network = core.network
        network.register_handler(PacketHeader.TOPO, TopoPacketHandler(self))
        network.register_handler(PacketHeader.HELLO, HelloPacketHandler(self))

    def next_hop_of_controller(self, controller):
        try:
            return self._controllers[self._nexthop_of_controller[controller.get_id()]]
        except KeyError:
            raise ControllerNotFoundException('The nexthop of ' + str(controller) + ' is not found!')

    def next_hop_of_switch(self, switch):
        try:
            for cid in self._controllers_of_switch[switch.get_id()]:
                controller = self._controllers[cid]
                if controller.is_up():
                    return controller
        except KeyError:
            raise SwitchNotFoundException('The nexthop of ' + str(switch) + ' is not found!')
        else:
            raise SwitchNotFoundException('The nexthop of ' + str(switch) + ' is not found!')

    def get_neighbor_relation(self, controller):
        return self._relation_of_neighbor[controller.get_id()]

    def get_peer_controller(self):
        controller_set = set()
        for cid in self._neighbors_with_relation['peer']:
            if self._controllers[cid].is_up():
                controller_set.add(self._controllers[cid])
        return controller_set

    def get_provider_controller(self):
        controller_set = set()
        for cid in self._neighbors_with_relation['provider']:
            if self._controllers[cid].is_up():
                controller_set.add(self._controllers[cid])
        return controller_set

    def get_customer_controller(self):
        controller_set = set()
        for cid in self._neighbors_with_relation['customer']:
            if self._controllers[cid].is_up():
                controller_set.add(self._controllers[cid])
        return controller_set
