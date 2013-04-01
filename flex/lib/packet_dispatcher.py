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

    def handle(self, address, data):
        packet = self._transformer.data_to_packet(data)
        handler = self._handlers[packet.header.type]
        logger.debug('Received ' + str(packet.header.type) + ' ' + str(packet))
        return handler.handle(packet)
