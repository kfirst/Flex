'''
Created on 2013-3-30

@author: kfirst
'''

from flex.core import core
from flex.base.handler import PacketHandler

logger = core.get_logger()

class HelloPacketHandler(PacketHandler):

    def __init__(self, topology):
        self._topo = topology

    def __getattr__(self, name):
        return getattr(self._topo, name)

    def handle(self, packet):
        # TODO
        pass
