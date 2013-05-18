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
    发送时，通过network模块，将报文发送给指定的controller，
    若controller为自己或为空则直接转给关心该类型报文的模块。
    
    因此，Forwarding模块可以作为Controller间报文传递的渠道，
    也可以作为模块间交互信息的渠道
    '''

    def __init__(self, controller):
        self._myself = controller
        self._my_id = controller.get_id()
        self._my_address = controller.get_address()
        self._transformer = PacketTransformer()
        self._dispatcher = PacketDispatcher(self._transformer)

    def start(self):
        core.network.register_data_handler(self._dispatcher)

    def register_handler(self, packet_type, packet_handler):
        '''
        为某种报文类型注册Handler，当收到该类型的Packet时，会调用相应Handler的handle方法
        '''
        self._dispatcher.register_handler(packet_type, packet_handler)

    def forward(self, packet):
        '''
        若指定Controller，则向指定的Controller发送Packet。
        若不指定Controlller，则自己Controller内部关心该类型报文的模块将接收到该报文
        '''
        dst = packet.dst
        if not dst or dst.get_id() == self._my_id:
            return self._dispatch(packet)
        address = core.routing.get_address(dst)
        if address == self._my_address:
            return self._dispatch(packet)
        if address:
#            logger.debug('Sending Packet to %s (address: %s), %s' % (dst, address, packet))
            data = self._transformer.packet_to_data(packet)
            return core.network.send(address, data)
        else:
            logger.warning('Can not find address for %s' % (dst))

    def _dispatch(self, packet):
        '''
        向自己发送报文，为了简化模块的设计，模块与模块之间的通信可以使用该方法，
        该方法会直接调用关心该类型报文的Handler，而无需经过内核转发
        '''
        self._dispatcher._handle(packet)
