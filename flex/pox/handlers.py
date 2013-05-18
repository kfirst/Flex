'''
Created on 2013-3-27

@author: kfirst
'''

from pox.core import core as pox_core
from flex.core import core as flex_core
from flex.model.packet import *
import pox.openflow.libopenflow_01 as of
from flex.model.action import Action
from pox.lib.packet import ethernet


class ControlHandler(object):
    _connection_pool = {}
    _id_prefix = flex_core.myself.get_self_controller().get_id()

    ALL_SWITCHES = 'all'

    def __init__(self):
        self._switches_listened = {}

    def _create_and_send_packet(self, content):
        flex_core.controllerAdaptor.forward(content)

    def _switch_id(self, dpid):
        return '%s/%s' % (self._id_prefix, dpid)

    def _get_connection(self, switch):
        return self._connection_pool.get(switch.get_id())

    def add_switch(self, switch = None):
        if self._switches_listened == self.ALL_SWITCHES:
            return False
        elif switch is None:
            pox_core.openflow.addListeners(self)
            for switch in self._switches_listened:
                self._connection_pool.get(switch.get_id()).removeListeners(self._switches_listened[switch])
            self._switches_listened = self.ALL_SWITCHES
            return True
        elif switch not in self._switches_listened:
            try:
                listeners = self._connection_pool.get(switch.get_id()).addListeners(self)
                self._switches_listened[switch] = listeners
                return True
            except KeyError:
                pass
        return False


class ConnectionUpHandler(ControlHandler):

    def __init__(self):
        super(ConnectionUpHandler, self).__init__()

    def _handle_ConnectionUp(self, event):
        connection = event.connection
        switch_id = self._switch_id(event.dpid)
        self._connection_pool[switch_id] = connection
        content = ConnectionUpContent(Switch.deserialize(switch_id))
        self._create_and_send_packet(content)


class ConnectionDownHandler(ControlHandler):

    def __init__(self):
        super(ConnectionDownHandler, self).__init__()

    def _handle_ConnectionDown(self, event):
        switch_id = self._switch_id(event.dpid)
        del self._connection_pool[switch_id]
        content = ConnectionDownContent(Switch.deserialize(switch_id))
        self._create_and_send_packet(content)


class PacketInHandler(ControlHandler):

    def __init__(self):
        super(PacketInHandler, self).__init__()

    def _handle_PacketIn(self, event):
        switch_id = self._switch_id(event.dpid)
        content = PacketInContent(Switch.deserialize(switch_id))
        content.buffer_id = event.ofp.buffer_id
        content.port = event.port
        content.data = event.data
        self._create_and_send_packet(content)


class PacketOutHandler(ControlHandler):

    def __init__(self):
        super(PacketOutHandler, self).__init__()

    def handle(self, content):
        msg = of.ofp_packet_out()
        msg.buffer_id = content.buffer_id
        if msg.buffer_id is None:
            msg.data = content.data
        else:
            msg.data = b''
        msg.in_port = content.port
        msg.actions = [ActionHandler.HANDLER[action.type](action) for action in content.actions]
        switch = self._get_connection(content.dst)
        switch.send(msg)


class FLowModHandler(ControlHandler):

    def __init__(self):
        super(FLowModHandler, self).__init__()

    def handle(self, content):
        msg = of.ofp_flow_mod()
        msg.match = MatchHandler.HANDLER[content.match.type](content.match)
        msg.idle_timeout = content.idle_timeout
        msg.hard_timeout = content.hard_timeout
        msg.buffer_id = content.buffer_id
        msg.actions = [ActionHandler.HANDLER[action.type](action) for action in content.actions]
        msg.data = content.data
        switch = self._get_connection(content.dst)
        switch.send(msg)


class ActionHandler(object):

    HANDLER = None

    @classmethod
    def output(cls, action):
        return of.ofp_action_output(port = action.port)

ActionHandler.HANDLER = {
    Action.OUTPUT: ActionHandler.output,
}


class MatchHandler(object):

    HANDLER = None

    @classmethod
    def data(cls, match):
        packet = ethernet.ethernet(match.data)
        return of.ofp_match.from_packet(packet, match.port)

MatchHandler.HANDLER = {
    Match.DATA: MatchHandler.data,
}
