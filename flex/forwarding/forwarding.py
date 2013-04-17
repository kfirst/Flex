# encoding: utf-8
'''
Created on 2013-4-17

@author: kfirst
'''

from flex.base.module import Module
from flex.core import core
from flex.forwarding.packet_dispatcher import PacketDispatcher
from flex.forwarding.packet_transformer import PacketTransformer

logger = core.get_logger()

class Forwarding(Module):
    '''
    系统报文的接收和发送，
    接收时，通过检查报文的类型字段，将收到的报文转发关心该类型报文的模块；
    发送时，通过network模块，将报文发送给指定的controller，若controller为自己则直接转给关心该类型报文的模块。
    '''

    def __init__(self, controller):
        self._myself = controller
        self._transformer = PacketTransformer()
        self._dispatcher = PacketDispatcher(self._transformer)

    def start(self):
        core.network.register_data_handler(self._dispatcher)

    def register_handler(self, packet_type, packet_handler):
        '''
        为某种报文类型注册Handler，当收到该类型的Packet时，会调用相应Handler的handle方法
        '''
        self._dispatcher.register_handler(packet_type, packet_handler)

    def forward(self, packet, controller = None):
        '''
        向指定的Controller发送Packet
        '''
        self._track(packet, controller)
        if not controller or controller.get_address() == self._myself.get_address():
            return self._dispatch(packet)
        else:
            logger.debug('Sending Packet to ' + str(controller) + ', ' + str(packet))
            data = self._transformer.packet_to_data(packet)
            return core.network.send(controller.get_address(), data)

    def _dispatch(self, packet):
        '''
        向自己发送报文，为了简化模块的设计，模块与模块之间的通信可以只用该方法，
        该方法会直接调用关心该类型报文的Handler，而无需经过内核转发
        '''
        self._dispatcher._handle(packet)

    def _track(self, packet, controller):
        if not controller:
            controller = self._myself
        packet.tracker.track(self._myself, controller)
