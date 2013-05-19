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
#        self._packets = Queue.Queue(100)
#        self._start_thread()

    def register_handler(self, packet_type, packet_handler):
        self._handlers[packet_type] = packet_handler

    def handle(self, data):
        packet = self._transformer.data_to_packet(data)
#        self._packets.put(packet, False)
        return self._handle(packet)

    def _handle(self, packet):
        try:
            handler = self._handlers[packet.type]
            logger.debug('Received Packet from %s, %s' % (packet.src, packet))
            handler.handle_packet(packet)
        except KeyError:
            logger.warning('Received undefined Packet from %s, %s' % (packet.src, packet))

#    def _schedule(self):
#        while 1:
#            packet = self._packets.get()
#            self._handle(packet)
#
#    def _start_thread(self):
#        thread = threading.Thread(target = self._schedule)
#        thread.setDaemon(True)
#        thread.start()
