# encoding: utf-8
'''
Created on 2013-3-19

@author: fzm
'''

from flex.core import core
from flex.base.module import Module
from flex.model.packet import Packet
from flex.base.event import FlexUpEvent

logger = core.get_logger()

class NeighborMonitor(Module):
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
        for neighbor in self._relation_of_neighbor.keys():
            core.routing.add_address(neighbor, neighbor.get_address())

        from flex.neighbor_monitor.hello_packet_handler import HelloPacketHandler
        self.hello = HelloPacketHandler(self._myself, self._relation_of_neighbor, self._neighbors_with_relation)

        core.forwarding.register_handler(Packet.HELLO, self.hello)
        core.event.register_handler(FlexUpEvent, self.hello)

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
