'''
Created on 2013-4-22

@author: kfirst
'''

from flex.core import core
from flex.model.packet import Packet
from flex.lib.util import object_to_string

logger = core.get_logger()


class BaseSwitch(object):

    _api = None

    def __init__(self, switch):
        self._switch = switch

    def add_listeners(self, obj):
        self._api._add_hanlders(obj, self._switch)

    def __repr__(self):
        return object_to_string(self,
                switch = self._switch)


class AllSwitches(BaseSwitch):

    def __init__(self):
        super(AllSwitches, self).__init__(None)


class Switch(BaseSwitch):

    _switches = {}

    def __init__(self, switch):
        super(Switch, self).__init__(switch)

    @classmethod
    def get_switch(cls, switch):
        try:
            ret = cls._switches[switch]
        except KeyError:
            ret = cls(switch)
            cls._switches[switch] = ret
        return ret

    @property
    def connect_time(self):
        return core.routing.get_connect_time(self._switch)

    def send(self, message):
        content = message.to_content(self._switch)
        packet = Packet(Packet.CONTROL_FROM_API, content)
        core.forwarding.forward(packet)


class Port(object):

    FLOOD = 1


class OutputAction(object):

    def __init__ (self):
        self.port = None


class Match(object):

    def __init__(self):
        self.data = None
        self.port = None

    @classmethod
    def from_data(cls, data, port = None):
        match = cls()
        match.data = data
        match.port = port
        return match
