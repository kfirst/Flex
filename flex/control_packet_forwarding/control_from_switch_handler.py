'''
Created on 2013-4-6

@author: fzm
'''
from flex.core import core
from flex.base.handler import PacketHandler
from flex.model.packet import RegisterConcersContent, Packet
import random

logger = core.get_logger()

class ControlFromSwitchHandler(PacketHandler):

    ALL_SWITCHES = RegisterConcersContent.ALL_SWITCHES

    def __init__(self, self_controller, controller_concerns, algorithms):
        # {controller: {type: set(switch)}}
        self._myself = self_controller
        self._controller_concerns = controller_concerns
        self._algorithms = []
        for algorithm, parameters in algorithms.items():
            try:
                self._algorithms.append((getattr(self, algorithm), parameters))
            except AttributeError:
                logger.warning('Algorithm ' + algorithm + ' is not found!')

    def handle_packet(self, packet):
        logger.info('Control from switch packet received')
        control_type = packet.content.type
        switch = packet.content.src
        controller = packet.content.dst
        if controller:
            self._send_packet(packet, controller)
        else:
            controllers = self._get_all_controllers(control_type, switch)
            for algorithm, parameter in self._algorithms:
                controllers = algorithm(controllers, *parameter)
            for controller in controllers:
                self._send_packet(packet, controller)

    def _send_packet(self, packet, dst):
        packet.content.dst = dst
        if dst == self._myself:
            packet.type = Packet.LOCAL_TO_API
            core.forwarding.forward(packet)
        else:
            nexthop = core.topology.nexthop(dst)
            core.forwarding.forward(packet, nexthop)

    def _get_all_controllers(self, control_type, switch):
        controllers = set()
        for controller, types in self._controller_concerns.items():
            if types == self.ALL_SWITCHES or control_type in types:
                controllers.add(controller)
        return controllers

    def shortest_path(self, controllers):
        ret = []
        shorest = None
        for controller in controllers:
            distance = core.topology.distance(controller)
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
