'''
Created on 2013-3-30

@author: kfirst
'''

from flex.core import core
from flex.base.handler import PacketHandler

logger = core.get_logger()

class TopoPacketHandler(PacketHandler):

    def __init__(self, topology):
        self._topo = topology
        self._handlers = {
            "peer": self._handle_peer,
            "customer": self._handle_customer,
            "myself": self._handle_customer
        }

    def __getattr__(self, name):
        return getattr(self._topo, name)

    def _handle_peer(self, packet):
        cid_src = packet.content.controller.get_id()
        self._add_switches(cid_src, packet.content.switches_added, True)
        self._remove_switches(cid_src, packet.content.switches_removed)

    def _handle_customer(self, packet):
        cid_src = packet.content.controller.get_id()
        self._add_switches(cid_src, packet.content.switches_added, False)
        self._remove_switches(cid_src, packet.content.switches_removed)
        # network send packet
        myself = self._controllers[self._my_id]
        packet.content.controller = myself
        for cid in self._neighbors_with_relation['provider']:
            self._send_packet(cid, packet)
        for cid in self._neighbors_with_relation['peer']:
            self._send_packet(cid, packet)

    def _add_switches(self, cid, switches, at_end):
        for sw in switches:
            try:
                if cid not in self._controllers_of_switch[sw.get_id()]:
                    if at_end:
                        self._controllers_of_switch[sw.get_id()].append(cid)
                    else:
                        self._controllers_of_switch[sw.get_id()].insert(0, cid)
            except KeyError:
                self._controllers_of_switch[sw.get_id()] = [cid]
                self._connection_fds[sw.get_id()] = sw

    def _remove_switches(self, cid, switches):
        for sw in switches:
            try:
                controllers = self._controllers_of_switch[sw.get_id()]
                if cid in controllers:
                    controllers.remove(cid)
                if(not controllers):
                    del self._controllers_of_switch[sw.get_id()]
                    del self._connection_fds[sw.get_id()]
            except KeyError:
                logger.warning(str(sw) + ' is not found!');

    def _send_packet(self, cid, packet):
        dst = self._controllers[cid]
        core.forwarding.forward(packet, dst)

    def handle(self, packet):
        logger.debug('Topo packet received')
        cid = packet.content.controller.get_id()
        try:
            relation = self._relation_of_neighbor[cid]
        except KeyError:
            if(cid == self._my_id):
                relation = 'myself'
            else:
                logger.warning('There is no neighbor with id [' + cid + ']!')
                return
        try:
            self._handlers[relation](packet)
        except KeyError:
            logger.warning('There is no handler handled relation [' + relation + ']!')
            return

