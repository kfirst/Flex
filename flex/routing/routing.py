'''
Created on 2013-5-12

@author: kfirst
'''

from flex.core import core
from flex.base import event
from flex.base.module import Module
from flex.routing.controller_packet_handler import ControllerPacketHandler
from flex.model.packet import Packet, RoutingPacketContent


class Routing(Module):

    ROUTING = 'routing'

    def __init__(self):
        self.routing = {}

    def start(self):
        myself = core.myself.get_self_controller()
        self.controller = ControllerPacketHandler(myself, core.neighborMonitor)
        core.forwarding.register_handler(Packet.ROUTING, self.controller)
        core.event.register_handler(event.NeighborControllerUpEvent, self.controller)
        core.globalStorage.set(myself.get_id(), myself.get_address(), self.ROUTING)
        if core.has_component('api'):
            controllers_update = [(myself, set())]
            content = RoutingPacketContent(myself, controllers_update, [])
            packet = Packet(Packet.ROUTING, content)
            core.forwarding.forward(packet)

    def add_address(self, controller, address):
        self.routing[controller.get_id()] = address

    def get_address(self, controller):
        device_id = controller.get_id()
        try:
            return self.routing[device_id]
        except KeyError:
            address = core.globalStorage.get(device_id, self.ROUTING)
            if address:
                self.routing[device_id] = address
            return address

    def get_distance(self, controller):
        return self.controller.distance_of_device(controller)
