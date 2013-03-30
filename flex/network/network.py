# encoding: utf-8
'''
Created on 2013-3-19

@author: kfirst
'''

from flex.lib import packet_transformer as T
from flex.lib import packet_dispatcher as D
from flex.lib.network import network as N
from flex.core import core
from flex.base.exception import ConnectFailException
from flex.base.module import Module
import threading

logger = core.get_logger()

class Network(Module):

    def __init__(self, address, backlog):
        self._transformer = T.PacketTransformer()
        self._dispatcher = D.PacketDispatcher(self._transformer)
        self._network = N.Network(address, backlog, self._dispatcher)

    def register_handler(self, packet_type, packet_handler):
        self._dispatcher.register_handler(packet_type, packet_handler)

    def send(self, controller, packet):
        logger.debug('[Sending Packet to ' + controller + ']' + packet)
        data = self._transformer.packet_to_data(packet)
        try:
            self._network.send(controller.get_address(), data)
        except ConnectFailException, e:
            logger.warning(e)
            return False
        return True

    def _schedule(self):
        while(True):
            self._network.schedule(-1)

    def start(self):
        thread = threading.Thread(target = self._schedule)
        thread.setDaemon(True)
        thread.start()
