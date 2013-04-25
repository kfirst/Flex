# encoding: utf-8
'''
Created on 2013-4-6

@author: fzm
'''

from flex.core import core
from flex.base.handler import PacketHandler
from flex.model.packet import Packet, RegisterConcersContent

logger = core.get_logger()

class RegisterConcernsHandler(PacketHandler):

    ALL_SWITCHES = RegisterConcersContent.ALL_SWITCHES

    def __init__(self, controller_concerns):
        # {controller: {type: set(switch)}}
        self._controller_concerns = controller_concerns

    def handle_packet(self, packet):
        logger.debug('Register Concerns packet received')
        controller = packet.content.controller
        concern_types = packet.content.types
        new_concern_types = {}
        for concern_type, switches in concern_types.items():
            try:
                controller_concerns = self._controller_concerns[controller]
                try:
                    added_switches = controller_concerns[concern_type]
                    if added_switches != self.ALL_SWITCHES:
                        if switches != self.ALL_SWITCHES:
                            switches -= added_switches
                            if switches:
                                added_switches.update(switches)
                                new_concern_types[concern_type] = switches
                        else:
                            controller_concerns[concern_type] = self.ALL_SWITCHES
                            new_concern_types[concern_type] = switches
                except KeyError:
                    controller_concerns[concern_type] = switches
                    new_concern_types[concern_type] = switches
            except KeyError:
                self._controller_concerns[controller] = {concern_type: switches}
                new_concern_types[concern_type] = switches
        if new_concern_types:
            packet.content.types = new_concern_types
            self._send_to_neighbor(packet)
        if core.has_component('pox'):
            self._send_to_local(packet)

    def _send_to_neighbor(self, packet):
        topo = core.topology
        forwarding = core.forwarding
        customers = topo.get_customers()
        for customer in customers:
            forwarding.forward(packet, customer)
        peers = topo.get_peers()
        for peer in peers:
            forwarding.forward(packet, peer)

    def _send_to_local(self, packet):
        packet.type = Packet.LOCAL_CONCERN
        core.forwarding.forward(packet)
