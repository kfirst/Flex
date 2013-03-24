# encoding: utf-8
'''
Created on 2013-3-19

@author: kfirst
'''

from flex.lib import packet_transformer as T
from flex.lib import packet_dispatcher as D
from flex.lib.network import network as N

class Network(object):

    def __init__(self, controller):
        self._transformer = T.PacketTransformer()
        self._dispatcher = D.PacketDispatcher(self._transformer)
        address = controller.get_address()
        backlog = controller.get_backlog()
        self._network = N.Network(address, backlog, self._dispatcher)

    def register_handler(self, packet_type, packet_handler):
        self._dispatcher.register_handler(packet_type, packet_handler)

    def send(self, controller, packet):
        data = self._transformer.packet_to_data(packet)
        self._network.send(controller.get_address(), data)

    def schedule(self, timeout):
        self._network.schedule(timeout)
