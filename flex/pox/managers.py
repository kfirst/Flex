'''
Created on 2013-4-9

@author: kfirst
'''
from flex.base.handler import PacketHandler
from flex.model.packet import PoxPacketContent as Pox
from flex.model.packet import ApiPacketContent as Api
from flex.pox.handlers import *
from flex.core import core

logger = core.get_logger()

class ConcernManager(PacketHandler):

    _handler_name = {
        Pox.PACKET_IN: PacketInHandler,
        Pox.CONNECTION_UP: ConnectionUpHandler,
        Pox.CONNECTION_DOWN: ConnectionDownHandler
    }

    def __init__(self):
        self._handlers = {}

    def add(self, control_type, switch):
        try:
            handler = self._handlers[control_type]
        except KeyError:
            try:
                handler = self._handler_name[control_type]()
                self._handlers[control_type] = handler
            except KeyError:
                logger.error('Handler handled [%s] is not found' % control_type)
                return
        if handler.add_switch(switch):
            logger.debug('Add handler [%s] for %s' % (control_type, switch))
        else:
            logger.warning('Fail to add handler [%s] for %s' % (control_type, switch))


class ProcesserManager(PacketHandler):

    _handler_name = {
            Api.PACKET_OUT: PacketOutHandler,
            Api.FLOW_MOD: FLowModHandler
    }

    def __init__(self):
        self._handlers = {}
        core.forwarding.register_handler(Packet.CONTROL_FROM_API, self)

    def process(self, api_content):
        control_type = api_content.type
        try:
            handler = self._handlers[control_type]
        except KeyError:
            try:
                handler = self._handler_name[control_type]()
                self._handlers[control_type] = handler
            except KeyError:
                logger.error('Handler handled [%s] is not found' % control_type)
                return
        handler.handle(api_content)
