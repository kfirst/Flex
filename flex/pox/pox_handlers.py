'''
Created on 2013-3-27

@author: kfirst
'''

from pox.core import core as pox_core
from flex.core import core as flex_core
from flex.model.packet import Packet, PacketHeader, TopologyPacketContent

class TopologyHandler():

    def __init__(self, switch_pool, self_controller):
        self._pool = switch_pool
        self._myself = self_controller
        pox_core.openflow.addListeners(self)

    def _handle_ConnectionUp(self, event):
        switch = event.connection
        self._pool.set(event.dpid, switch)
        packet = self._create_topo_packet(switch, True)
        flex_core.network.dispatch(packet)

    def _handle_ConnectionDown(self, event):
        switch = event.connection
        self._pool.remove(event.dpid)
        packet = self._create_topo_packet(switch, False)
        flex_core.network.dispatch(packet)

    def _create_topo_packet(self, switch, add = True):
        added = set()
        removed = set()
        if add:
            added.add(switch)
        else:
            removed.add(switch)
        content = TopologyPacketContent(self._myself, added, removed)
        return Packet(PacketHeader.TOPO, content)
