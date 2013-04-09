'''
Created on 2013-4-9

@author: kfirst
'''
from flex.base.handler import PacketHandler
from flex.model.packet import ControlPacketContent as Control
from flex.pox.pox_handlers import *
from flex.core import core

logger = core.get_logger()

class ConcernHandler(PacketHandler):

    def __init__(self, self_controller):
        self._myself = self_controller
        self._handlers = {}
        self._handlers_name = {
            Control.CONNECTION_UP: ConnectionUpHandler,
            Control.CONNECTION_DOWN: ConnectionDownHandler
        }

    def handle(self, packet):
        types = packet.content.type
        for control_type in types:
            if control_type not in self._handlers:
                try:
                    handler_class = self._handlers_name[control_type]
                except KeyError:
                    logger.error('No handler for type [' + control_type + '] in ' + str(packet))
                    return
                self._handlers[control_type] = handler_class(self._myself)


class LocalHandler(PacketHandler):

    def __init__(self, switch_pool):
        self._pool = switch_pool

    def handle(self, packet):
        control_type = packet.content.type
        try:
            func = getattr(self, control_type)
        except AttributeError:
            logger.error('No handler for type [' + control_type + '] in ' + packet)
        func(packet.content)
