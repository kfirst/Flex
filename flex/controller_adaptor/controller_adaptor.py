'''
Created on 2013-5-12

@author: kfirst
'''

from flex.base.module import Module
from flex.base.handler import PacketHandler, StorageHandler
from flex.core import core
from flex.model.packet import Packet
import random
from flex.api.api import Api

logger = core.get_logger()


class ControllerAdaptor(Module, PacketHandler, StorageHandler):

    CONCERN = Api.CONCERN
    GLOBAL = Api.GLOBAL

    def __init__(self, app_name, algorithms):
        self.app = getattr(core, app_name)
        self.controllers = {}
        self._algorithms = []
        self._myself = core.myself.get_self_controller()
        for algorithm, parameters in algorithms.items():
            try:
                self._algorithms.append((getattr(self, algorithm), parameters))
            except AttributeError:
                logger.warning('Algorithm ' + algorithm + ' is not found!')

    def start(self):
        core.forwarding.register_handler(Packet.STORAGE, self)
        core.storage.listen(self.GLOBAL, self,)

    def handle_storage(self, key, value, type):
        pass
#        controller = packet.content.controller
#        concern_types = packet.content.types
#        for concern_type, switches in concern_types.items():
#            try:
#                switch_controllers = self.controllers[concern_type]
#                if switches == self.ALL_SWITCHES:
#                    try:
#                        switch_controllers[switches].add(controller)
#                    except KeyError:
#                        switch_controllers[switches] = set([controller])
#                else:
#                    for switch in switches:
#                        try:
#                            switch_controllers[switch].add(controller)
#                        except KeyError:
#                            switch_controllers[switch] = set([controller])
#            except KeyError:
#                self.controllers[concern_type] = {switches: set([controller])}

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

