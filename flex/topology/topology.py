# encoding: utf-8
'''
Created on 2013-3-19

@author: fzm
'''

from flex.core import core
from flex.base.module import Module
from flex.base.exception import SwitchNotFoundException, \
    ControllerNotFoundException
from flex.model.packet import Packet
from flex.base import event
from flex.model.device import Switch, Controller

logger = core.get_logger()

class Topology(Module):
    '''
    用于维护邻居信息和邻居可达的Switch与Controller信息。详见:
    @HelloPacketHandler
    @SwitchPacketHandler
    
    TODO
    1. 定时发送keepalive信息，检测邻居是否活着，若Down了产生NeighborControllerDown事件；
    2. 若新Switch出现，产生SwitchUp事件；
    3. 若Switch消失（即该Switch没有Controller可达），产生SwitchDown事件；
    '''

    PROVIDER = 'provider'
    PEER = 'peer'
    CUSTOMER = 'customer'

    def __init__(self):
        self._myself = None
        self._relation_of_neighbor = {}
        self._neighbors_with_relation = {}

    def start(self):
        from flex.topology.hello_packet_handler import HelloPacketHandler
        self.hello = HelloPacketHandler(self._myself, self._relation_of_neighbor, self._neighbors_with_relation)
        from flex.topology.switch_packet_handler import SwitchPacketHandler
        self.switch = SwitchPacketHandler(self._myself, self._relation_of_neighbor, self._neighbors_with_relation)
        from flex.topology.controller_packet_handler import ControllerPacketHandler
        self.controller = ControllerPacketHandler(self._myself, self._relation_of_neighbor, self._neighbors_with_relation)

        core.forwarding.register_handler(Packet.HELLO, self.hello)
        core.forwarding.register_handler(Packet.TOPO_SWITCH, self.switch)
        core.event.register_handler(event.NeighborControllerUpEvent, self.switch)
        core.forwarding.register_handler(Packet.TOPO_CONTROLLER, self.controller)
        core.event.register_handler(event.NeighborControllerUpEvent, self.controller)

    def nexthop(self, device):
        if isinstance(device, Switch):
            try:
                return self.switch.nexthop_of_device(device)
            except KeyError:
                raise SwitchNotFoundException(str(device) + ' is not found!')
        elif isinstance(device, Controller):
            try:
                return self.controller.nexthop_of_device(device)
            except KeyError:
                raise ControllerNotFoundException(str(device) + ' is not found!')

    def distance(self, device):
        if isinstance(device, Switch):
            try:
                return self.switch.distance_of_device(device)
            except KeyError:
                raise SwitchNotFoundException(str(device) + ' is not found!')
        elif isinstance(device, Controller):
            try:
                return self.controller.distance_of_device(device)
            except KeyError:
                raise ControllerNotFoundException(str(device) + ' is not found!')

    def get_neighbor_relation(self, controller):
        return self.hello.get_neighbor_relation(controller)

    def get_neighbors(self):
        return self.hello.get_neighbors()

    def get_peers(self):
        return self.hello.get_peers()

    def get_providers(self):
        return self.hello.get_providers()

    def get_customers(self):
        return self.hello.get_customers()
