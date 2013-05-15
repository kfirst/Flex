'''
Created on 2013-5-12

@author: kfirst
'''

from flex.core import core
from flex.base import event
from flex.base.module import Module
from flex.routing.controller_packet_handler import ControllerPacketHandler
from flex.model.packet import Packet, RoutingPacketContent
from flex.base.handler import EventHandler
import time


class Routing(Module, EventHandler):

    ROUTING = 'routing'
    ROUTING_TIME = 'routing_time'

    def __init__(self):
        self.routing = {}

    def start(self):
        self.myself = core.myself.get_self_controller()
        self.controller = ControllerPacketHandler(self.myself, core.neighborMonitor)
        self.connected(self.myself, self.myself.get_address())
        core.forwarding.register_handler(Packet.ROUTING, self.controller)
        core.event.register_handler(event.NeighborControllerUpEvent, self.controller)
        core.event.register_handler(event.FlexUpEvent, self)

    def handle_event(self, event):
        if core.has_component('api'):
            controllers_update = [(self.myself, set())]
            content = RoutingPacketContent(self.myself, controllers_update, [])
            packet = Packet(Packet.ROUTING, content)
            core.forwarding.forward(packet)

    def add_address(self, device, address):
        self.routing[device.get_id()] = address
        core.globalStorage.set(device.get_id(), address, self.ROUTING)

    def connected(self, device, address):
        self.add_address(device, address)
        core.globalStorage.set(device.get_id(), time.time(), self.ROUTING_TIME)

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

    def get_connect_time(self, device):
        return core.globalStorage.get(device.get_id(), self.ROUTING_TIME)
