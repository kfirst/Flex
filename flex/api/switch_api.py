'''
Created on 2013-5-15

@author: kfirst
'''

from flex.core import core
from flex.base.module import Module
from flex.model.packet import Packet


class SwitchApi(Module):

    def __init__(self):
        self._packet = Packet(Packet.CONTROL_FROM_API, None)
        self._packet.src = core.myself.get_self_controller()
        self._connect_time = {}

    def get_connect_time(self, switch):
        try:
            time = self._connect_time[switch]
        except KeyError:
            time = core.routing.get_connect_time(switch)
            self._connect_time[switch] = time
        return time

    def send_to(self, switch, message):
        message.dst = switch
        self._packet.content = message
        self._packet.dst = switch
        core.forwarding.forward(self._packet)
