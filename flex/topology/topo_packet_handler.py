'''
Created on 2013-3-30

@author: kfirst
'''

from flex.core import core
from flex.model.device import Switch
from flex.base.handler import PacketHandler

logger = core.get_logger()

class TopoPacketHandler(PacketHandler):

    def __init__(self, topology):
        self._topo = topology
        self._handlers = {
            "peer": self._handle_peer,
            "customer": self._handle_customer
        }

    def __getattr__(self, name):
        return getattr(self._topo, name)

    def _handler_peer(self, packet):
        cid_src = packet.content.controller.get_id()
        self._add_switches(cid_src, packet.content.switches_added, True)
        self._remove_switches(cid_src, packet.content.switches_removed)

    def _handler_customer(self, packet):
        cid_src = packet.content.controller.get_id()
        self._add_switches(cid_src, packet.content.switches_added, False)
        self._remove_switches(cid_src, packet.content.switches_removed)
        # network send packet
        myself = self._controllers[self._my_id]
        packet.content.controller = myself
        packet.header.path.append(myself)
        for cid in self._neighbors_with_relation['provider']:
            self._send_packet(cid, packet)
        for cid in self._neighbors_with_relation['peer']:
            self._send_packet(cid, packet)

    def _add_switches(self, cid, sids, at_end):
        for sid in sids:
            try:
                if at_end:
                    self._controllers_of_switch[sid].append(cid)
                else:
                    self._controllers_of_switch[sid].insert(0, cid)
            except KeyError:
                self._controllers_of_switch[sid] = [cid]
                self._switches[sid] = Switch(sid)

    def _remove_switches(self, cid, sids):
        for sid in sids:
            try:
                controllers = self._controllers_of_switch[sid]
                controllers.remove(cid)
                if(not controllers):
                    del self._controllers_of_switch[sid]
                    del self._switches[sid]
            except KeyError:
                logger.warning('Switch(' + sid + ') is not found!');

    def _send_packet(self, cid, packet):
        dst = self._controllers[cid]
        packet.header.dst = dst
        core.network.send(dst, packet)

    def handle(self, packet):
        cid = packet.content.controller.get_id()
        try:
            relation = self._relation_of_neighbor[cid]
        except KeyError:
            logger.warning('There is no neighbor with id [' + cid + ']!')
            return
        try:
            self._handlers[relation](packet)
        except KeyError:
            logger.warning('There is no handler handled relation [' + relation + ']!')
            return

