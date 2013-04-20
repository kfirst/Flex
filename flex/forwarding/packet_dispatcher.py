'''
Created on 2013-3-18

@author: kfirst
'''

from flex.base.handler import DataHandler
from flex.core import core

logger = core.get_logger()

class PacketDispatcher(DataHandler):

    def __init__(self, packet_transformer):
        self._handlers = {}
        self._transformer = packet_transformer

    def register_handler(self, packet_type, packet_handler):
        self._handlers[packet_type] = packet_handler

    def handle(self, data):
        packet = self._transformer.data_to_packet(data)
        return self._handle(packet)

    def _handle(self, packet):
        try:
            handler = self._handlers[packet.type]
            logger.debug('Received Packet from ' + str(packet.tracker.src) + ', ' + str(packet))
            handler.handle_packet(packet)
            return True
        except KeyError:
            logger.warning('Received undefined Packet from ' + str(packet.tracker.src) + ', ' + str(packet))
            return False
