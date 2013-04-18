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

    def __init__(self):
        self._handlers = {}
        self._handlers_name = {
            Control.PACKET_IN: PacketInHandler
        }
        core.network.register_handler(Packet.LOCAL_CONCERN, self)

    def handle(self, packet):
        types = packet.content.types
        for control_type in types:
            switches = types[control_type]
            try:
                handler = self._handlers[control_type]
            except KeyError:
                try:
                    handler = self._handlers_name[control_type]()
                    self._handlers[control_type] = handler
                except KeyError:
                    logger.error('Handler handled [' + control_type + '] is not found in ' + str(packet))
                    continue
            added = handler.add_switches(switches)
            logger.debug('Add handler handled [' + control_type + '] for ' + added + ' in ' + switches)


class LocalHandler(PacketHandler):

    def __init__(self):
        core.network.register_handler(Packet.LOCAL_TO_POX, self)

    def handle(self, packet):
        control_type = packet.content.type
        try:
            func = getattr(self, control_type)
        except AttributeError:
            logger.error('No handler for type [' + control_type + '] in ' + str(packet))
        func(packet.content)
