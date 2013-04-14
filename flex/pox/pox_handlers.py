'''
Created on 2013-3-27

@author: kfirst
'''

from pox.core import core as pox_core
from flex.core import core as flex_core
from flex.model.packet import *
from flex.model.device import Switch

class ConnectionPool(object):

    def __init__(self):
        self._connections = {}

    def set(self, key, switch):
        self._connections[key] = switch

    def get(self, key):
        return self._connections[key]

    def remove(self, key):
        del self._connections[key]


class ControlHandler(object):
    _pool = ConnectionPool()
    _myself = flex_core.myself.get_self_controller()

    def _create_and_send_packet(self, content, packet_type = Packet.CONTROL_FROM_SWITCH):
        packet = Packet(packet_type, content)
        flex_core.network.send(self._myself, packet)

    def _switch_id(self, dpid):
        return str(self._myself.get_id()) + '_' + str(dpid)


class TopologyHandler(ControlHandler):

    def __init__(self):
        pox_core.openflow.addListeners(self)

    def _handle_ConnectionUp(self, event):
        connection = event.connection
        switch_id = self._switch_id(event.dpid)
        self._pool.set(switch_id, connection)
        packet_content = self._create_topo_content(Switch(switch_id), True)
        self._create_and_send_packet(packet_content, Packet.TOPO)

    def _handle_ConnectionDown(self, event):
        switch_id = self._switch_id(event.dpid)
        self._pool.remove(switch_id)
        packet_content = self._create_topo_content(Switch(switch_id), False)
        self._create_and_send_packet(packet_content, Packet.TOPO)

    def _create_topo_content(self, switch, add = True):
        added = set()
        removed = set()
        if add:
            added.add(switch)
        else:
            removed.add(switch)
        return TopologyPacketContent(self._myself, added, removed)


class ConnectionUpHandler(ControlHandler):

    def __init__(self):
        pox_core.openflow.addListeners(self)

    def _handle_ConnectionUp(self, event):
        switch = Switch(self._switch_id(event.dpid))
        content = ConnectionUpContent(switch)
        self._create_and_send_packet(content)


class ConnectionDownHandler(ControlHandler):

    def __init__(self):
        pox_core.openflow.addListeners(self)

    def _handle_ConnectionDown(self, event):
        switch = Switch(self._switch_id(event.dpid))
        content = ConnectionDownContent(switch)
        self._create_and_send_packet(content)
