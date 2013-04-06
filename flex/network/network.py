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
    '''
    网络模块，负责收发Packet
    '''

    def __init__(self, controller, backlog):
        self._transformer = T.PacketTransformer()
        self._dispatcher = D.PacketDispatcher(self._transformer)
        self._myself = controller
        self._network = N.Network(controller.get_address(), backlog, self._dispatcher)

    def register_handler(self, packet_type, packet_handler):
        '''
        为某种报文类型注册Handler，当收到该类型的Packet时，会调用相应Handler的handle方法
        '''
        self._dispatcher.register_handler(packet_type, packet_handler)

    def send(self, controller, packet):
        '''
        向指定的Controller发送Packet
        '''
        self._check_header(controller, packet)
        logger.debug('Sending Packet to ' + str(controller) + ', ' + str(packet))
        data = self._transformer.packet_to_data(packet)
        try:
            self._network.send(controller.get_address(), data)
        except ConnectFailException, e:
            logger.warning(e)
            return False
        return True

    def dispatch(self, packet):
        '''
        向自己发送报文，为了简化模块的设计，模块与模块之间的通信可以只用该方法，
        该方法会直接调用关心该类型报文的Handler，而无需经过内核转发
        '''
        self._dispatcher._handle(packet)

    def _check_header(self, controller, packet):
        packet.header.src = self._myself
        packet.header.dst = controller
        path = packet.header.path
        if not path or path[-1] != self._myself:
            path.append(self._myself)

    def _schedule(self):
        while(True):
            self._network.schedule(-1)

    def start(self):
        thread = threading.Thread(target = self._schedule)
        thread.setDaemon(True)
        thread.start()
