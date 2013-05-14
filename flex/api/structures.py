'''
Created on 2013-4-22

@author: kfirst
'''

from flex.core import core
from flex.model.packet import Packet
import pox.openflow.libopenflow_01 as of
from flex.lib.util import object_to_string

logger = core.get_logger()

class BaseSwitch(object):

    def __init__(self, api, switch):
        self._api = api
        self._switch = switch

    def __repr__(self):
        return object_to_string(self,
                switch = self._switch)


class AllSwitches(BaseSwitch):

    def __init__(self, api):
        super(AllSwitches, self).__init__(api, None)

    def add_listeners(self, obj):
        self._api._add_hanlders(obj, self._switch)


class Switch(BaseSwitch):

    def __init__(self, api, switch):
        super(Switch, self).__init__(api, switch)

    def add_listeners(self, obj):
        self._api._add_hanlders(obj, set([self._switch]))

    @property
    def connect_time(self):
        return core.topology.connect_time(self._switch)

    def send(self, message):
        content = message.to_content(self._switch)
        packet = Packet(Packet.CONTROL_FROM_API, content)
        core.forwarding.forward(packet)


class Port(object):

    @staticmethod
    def flood():
        return of.OFPP_FLOOD


class OutputAction(of.ofp_action_output):

    def __init__ (self, **kw):
        super(OutputAction, self).__init__(**kw)


class Match(of.ofp_match):
    pass
