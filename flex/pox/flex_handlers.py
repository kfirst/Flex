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

    _handler_name = {
        Control.PACKET_IN: PacketInHandler,
        Control.CONNECTION_UP: ConnectionUpHandler,
        Control.CONNECTION_DOWN: ConnectionDownHandler
    }

    def __init__(self):
        self._handlers = {}
        core.forwarding.register_handler(Packet.LOCAL_CONCERN, self)

    def handle_packet(self, packet):
        logger.info('Local Concerns packet received')
        types = packet.content.types
        for control_type in types:
            switches = types[control_type]
            try:
                handler = self._handlers[control_type]
            except KeyError:
                try:
                    handler = self._handler_name[control_type]()
                    self._handlers[control_type] = handler
                except KeyError:
                    logger.error('Handler handled [' + control_type + '] is not found in ' + str(packet))
                    continue
            added = handler.add_switches(switches)
            logger.debug('Add handler handled [' + control_type + '] for ' + str(added) + ' in ' + str(switches))


class LocalHandler(PacketHandler):

    _handler_name = {
            Control.PACKET_OUT: PacketOutHandler,
            Control.FLOW_MOD: FLowModHandler
    }

    def __init__(self):
        self._handlers = {}
        core.forwarding.register_handler(Packet.LOCAL_TO_POX, self)


    def handle_packet(self, packet):
        control_type = packet.content.type
        logger.info('Local to pox [' + control_type + '] packet received')
        try:
            handler = self._handlers[control_type]
        except KeyError:
            try:
                handler = self._handler_name[control_type]()
                self._handlers[control_type] = handler
            except KeyError:
                logger.error('Handler handled [' + control_type + '] is not found in ' + str(packet))
        handler.handle(packet.content)
