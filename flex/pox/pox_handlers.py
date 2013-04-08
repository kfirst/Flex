'''
Created on 2013-3-27

@author: kfirst
'''

from pox.core import core as pox_core
from flex.core import core as flex_core
from flex.model.packet import *
from flex.model.device import Switch

class TopologyHandler(object):

    def __init__(self, switch_pool, self_controller):
        self._pool = switch_pool
        self._myself = self_controller
        pox_core.openflow.addListeners(self)

    def _handle_ConnectionUp(self, event):
        connection = event.connection
        self._pool.set(event.dpid, connection)
        packet = self._create_topo_packet(Switch(event.dpid), True)
        flex_core.network.send(self._myself, packet)

    def _handle_ConnectionDown(self, event):
        switch = event.connection
        self._pool.remove(event.dpid)
        packet = self._create_topo_packet(switch, False)
        flex_core.network.send(self._myself, packet)

    def _create_topo_packet(self, switch, add = True):
        added = set()
        removed = set()
        if add:
            added.add(switch)
        else:
            removed.add(switch)
        content = TopologyPacketContent(self._myself, added, removed)
        return Packet(Packet.TOPO, content)


class ControlHandler(object):

    def __init__(self, self_controller):
        self._myself = self_controller

    def _create_and_send_packet(self, content):
        packet = Packet(Packet.CONTROL_FROM_SWITCH, content)
        flex_core.network.send(self._myself, packet)


class ConnectionUpHandler(ControlHandler):

    def __init__(self, self_controller):
        super(ConnectionUpHandler, self).__init__(self_controller)
        pox_core.openflow.addListeners(self)

    def _handle_ConnectionUp(self, event):
        switch = Switch(event.dpid)
        content = ConnectionUpContent(switch)
        self._create_and_send_packet(content)


class ConnectionDownHandler(ControlHandler):

    def __init__(self, self_controller):
        super(ConnectionDownHandler, self).__init__(self_controller)
        pox_core.openflow.addListeners(self)

    def _handle_ConnectionDown(self, event):
        switch = Switch(event.dpid)
        content = ConnectionDownContent(switch)
        self._create_and_send_packet(content)
