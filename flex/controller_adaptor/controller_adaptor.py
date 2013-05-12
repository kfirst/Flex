'''
Created on 2013-5-12

@author: kfirst
'''

from flex.base.module import Module
from flex.base.handler import PacketHandler
from flex.core import core
from flex.model.packet import Packet, RegisterConcersContent
import random

logger = core.get_logger()


class ControllerAdaptor(Module, PacketHandler):

    ALL_SWITCHES = RegisterConcersContent.ALL_SWITCHES

    def __init__(self, app_name, algorithms):
        core.forwarding.register_handler(Packet.LOCAL_CONCERN, self)
        self.app = getattr(core, app_name)
        self.controllers = {}
        self._algorithms = []
        self._myself = core.myself.get_self_controller()
        for algorithm, parameters in algorithms.items():
            try:
                self._algorithms.append((getattr(self, algorithm), parameters))
            except AttributeError:
                logger.warning('Algorithm ' + algorithm + ' is not found!')

    def handle_packet(self, packet):
        pass

    def forward(self, packet):
        switch = packet.src
        type = packet.content.type
        controllers = self._get_controllers(type, switch)
        self._send_packet(controllers, packet)

    def _get_controllers(self, type, switch):
        controllers = set()
        try:
            controllers.update(self.controllers[type][self.ALL_SWITCHES])
        except KeyError:
            pass
        try:
            controllers.update(self.controllers[type][switch])
        except KeyError:
            pass
        return controllers

    def _send_packet(self, controllers, packet):
        for algorithm, parameter in self._algorithms:
                controllers = algorithm(controllers, *parameter)
        for controller in controllers:
            packet.src = self._myself
            packet.dst = controller
            core.forwarding.forward(packet)

    def shortest_path(self, controllers):
        ret = []
        shorest = None
        for controller in controllers:
            distance = core.routing.get_distance(controller)
            if shorest == None or distance < shorest:
                shorest = distance
                ret = [controller]
            elif distance == shorest:
                ret.append(controller)
        return ret

    def first(self, controllers):
        return [controllers[0]]

    def sample(self, controllers, size):
        return random.sample(controllers, min(len(controllers), size))

