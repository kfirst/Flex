'''
Created on 2013-4-22

@author: kfirst
'''
from flex.base.module import Module
from flex.model.packet import TopologyControllerPacketContent, Packet
from flex.core import core

class Api(Module):

    def __init__(self, self_controller):
        self._myself = self_controller

    def start(self):
        controllers_update = [(self._myself, set())]
        content = TopologyControllerPacketContent(self._myself, controllers_update, [])
        packet = Packet(Packet.TOPO_CONTROLLER, content)
        core.forwarding.forward(packet)
