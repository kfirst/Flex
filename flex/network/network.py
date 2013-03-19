# encoding: utf-8
'''
Created on 2013-3-19

@author: kfirst
'''

from flex.lib import packet_transformer as T
from flex.lib import packet_dispatcher as D
from flex.lib.network import network as N

class Network(object):

    def __init__(self):
        self._transformer = T.PacketTransformer()
        self._dispatcher = D.PacketDispatcher(self._transformer)
        self._network = N.Network()
