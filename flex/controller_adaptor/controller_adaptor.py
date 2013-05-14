'''
Created on 2013-5-12

@author: kfirst
'''

from flex.base.module import Module
from flex.base.handler import PacketHandler, StorageHandler
from flex.core import core
from flex.model.packet import Packet
from flex.api.api import Api
from flex.model.device import Device
from flex.controller_adaptor.selection_algorithms import SelectionAlgorithms

logger = core.get_logger()


class ControllerAdaptor(Module, PacketHandler, StorageHandler):

    LOCAL_CONCERN = Api.LOCAL_CONCERN
    GLOBAL_CONCERN = Api.GLOBAL_CONCERN

    def __init__(self, app_name, algorithms):
        self.app = getattr(core, app_name)
        self._global_controllers = {}
        self._local_controllers = {}
        self._algorithms = []
        self._myself = core.myself.get_self_controller()
        for algorithm, parameters in algorithms.items():
            try:
                self._algorithms.append((getattr(SelectionAlgorithms, algorithm), parameters))
            except AttributeError:
                logger.warning('Algorithm ' + algorithm + ' is not found!')

    def start(self):
        core.forwarding.register_handler(Packet.STORAGE, self)
        core.storage.listen_domain(self, self.GLOBAL_CONCERN, True)

    def handle_storage(self, key, value, domain, type):
        if domain == self.GLOBAL_CONCERN:
            controller = Device.deserialize(key)
            for concern_type in value:
                try:
                    self._global_controllers[concern_type].add(controller)
                except KeyError:
                    self._global_controllers[concern_type] = set([controller])
        else:
            pass

    def forward(self, packet):
        switch = packet.src
        type = packet.content.type
        controllers = self._get_controllers(type, switch)
        for algorithm, parameter in self._algorithms:
            controllers = algorithm(controllers, *parameter)
        packet.src = self._myself
        for controller in controllers:
            self._send_packet(controller, packet)

    def _get_controllers(self, type, switch):
        controllers = set()
        try:
            controllers.update(self._global_controllers[type])
        except KeyError:
            pass
        try:
            controllers.update(self._local_controllers[type][switch])
        except KeyError:
            pass
        return controllers

    def _send_packet(self, controller, packet):
        packet.dst = controller
        core.forwarding.forward(packet)
