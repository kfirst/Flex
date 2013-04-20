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
        self._connection_fds = {}

    def set(self, key, switch):
        self._connection_fds[key] = switch

    def get(self, key):
        return self._connection_fds[key]

    def remove(self, key):
        del self._connection_fds[key]


class ControlHandler(object):
    _pool = ConnectionPool()
    _myself = flex_core.myself.get_self_controller()

    ALL_SWITCHES = RegisterConcersContent.ALL_SWITCHES

    def __init__(self):
        self._switches = {}

    def _create_and_send_packet(self, content, packet_type = Packet.CONTROL_FROM_SWITCH):
        packet = Packet(packet_type, content)
        flex_core.forwarding.forward(packet)

    def _switch_id(self, dpid):
        return str(self._myself.get_id()) + '_' + str(dpid)

    def add_switches(self, switches = []):
        added = []
        if self._switches == self.ALL_SWITCHES:
            pass
        elif switches == self.ALL_SWITCHES:
            pox_core.openflow.addListeners(self)
            for switch in self._switches:
                self._pool.get(switch.get_id()).removeListeners(self._switches[switch])
            self._switches = self.ALL_SWITCHES
        else:
            for switch in switches:
                if switch not in self._switches:
                    try:
                        listeners = self._pool.get(switch.get_id()).addListeners(self)
                        self._switches[switch] = listeners
                        added.append(switch)
                    except KeyError:
                        pass
        return added


class TopologyHandler(ControlHandler):

    def __init__(self):
        super(TopologyHandler, self).__init__()
        pox_core.openflow.addListeners(self)

    def _handle_ConnectionUp(self, event):
        connection = event.connection
        switch_id = self._switch_id(event.dpid)
        self._pool.set(switch_id, connection)
        packet_content = self._create_topo_content(Switch(switch_id), True)
        self._create_and_send_packet(packet_content, Packet.TOPO_SWITCH)

    def _handle_ConnectionDown(self, event):
        switch_id = self._switch_id(event.dpid)
        self._pool.remove(switch_id)
        packet_content = self._create_topo_content(Switch(switch_id), False)
        self._create_and_send_packet(packet_content, Packet.TOPO_SWITCH)

    def _create_topo_content(self, switch, add = True):
        added = []
        removed = []
        if add:
            added.append((switch, set()))
        else:
            removed.append(switch)
        return TopologySwitchPacketContent(self._myself, added, removed)


class PacketInHandler(ControlHandler):

    def _handle_PacketIn(self, event):
        switch = Switch(self._switch_id(event.dpid))
        port = event.port
        data = event.data
        content = PacketInContent(switch, port, data)
        self._create_and_send_packet(content)
