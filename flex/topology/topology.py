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
    '''
    用于维护邻居信息和邻居可达的Switch信息。
    
    维护邻居信息的工作原理是：
    当Controller1的topology模块启动起来后，将向其所有的邻居发送Hello报文；
    当Controller2收到Hello报文时，它就认为Controller1 Up了，
    并产生NeighborControllerUp事件，然后回复一个response Hello报文；
    当Controller1收到response Hello报文时，它就认为Controller2 Up了，
    并产生NeighborControllerUp事件。
    
    维护邻居可达的Switch信息的工作原理是：
    当Controller的一个peer或provider Controller2 Up时，
    Controller会将其邻居可达的所有Switch的信息按照拥有者为自己发送给Up的Controller；
    当一个Controller收到Switch信息后，首先更新自己邻居可达Switch的信息，
    然后检查发送者的身份，provider（不应为provider），什么都不做，
    若为peer或customer，则将自己信息中更新的Switch（注意不是收到报文中的全部Switch）
    按照拥有者为自己发给除发送者外的已经up的peer或provider。
    
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
        return set(self._relation_of_neighbor[controller.get_id()])

    def get_neighbors(self):
        return self._filter_controller(self._relation_of_neighbor.keys())

    def get_peers(self):
        return self._filter_controller(self._neighbors_with_relation[self.PEER])

    def get_providers(self):
        return self._filter_controller(self._neighbors_with_relation[self.PROVIDER])

    def get_customers(self):
        return self._filter_controller(self._neighbors_with_relation[self.CUSTOMER])

    def _filter_controller(self, controller_ids):
        controller_set = set()
        for cid in controller_ids:
            controller = self._controllers[cid]
            if controller.is_up():
                controller_set.add(controller)
        return controller_set
