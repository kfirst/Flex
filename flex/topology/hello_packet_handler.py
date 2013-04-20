# encoding: utf-8
'''
Created on 2013-3-30

@author: kfirst
'''

from flex.core import core
from flex.base.handler import PacketHandler
from flex.base.event import NeighborControllerUpEvent
from flex.model.packet import HelloPacketContent, Packet

logger = core.get_logger()

class HelloPacketHandler(PacketHandler):
    '''
    维护邻居信息的工作原理是：
    当Controller1的topology模块启动起来后，将向其所有的邻居发送Hello报文；
    当Controller2收到Hello报文时，它就认为Controller1 Up了，
    并产生NeighborControllerUp事件，然后回复一个response Hello报文；
    当Controller1收到response Hello报文时，它就认为Controller2 Up了，
    并产生NeighborControllerUp事件。
    '''

    def __init__(self, myself, relation_of_neighbor):
        self._myself = myself
        self._relation_of_neighbor = relation_of_neighbor
        hello_packet_content = HelloPacketContent(self._myself)
        self._packet = Packet(Packet.HELLO, hello_packet_content)
        # send hello packet
        hello_packet = self._make_hello_packet()
        for neighbor in self._relation_of_neighbor:
            self._send_packet(hello_packet, neighbor)

    def handle_packet(self, packet):
        logger.debug('Hello packet received')

        up_controller = packet.content.controller
        try:
            relation = self._relation_of_neighbor[up_controller]
        except KeyError:
            logger.warning('There is no neighbor ' + str(up_controller))
            return
        if not packet.content.response:
            hello_packet = self._make_hello_packet(True)
            self._send_packet(hello_packet, up_controller)

        core.event.happen(NeighborControllerUpEvent(up_controller, relation))

    def _make_hello_packet(self, response = False):
        self._packet.content.response = response
        return self._packet

    def _send_packet(self, packet, dst):
        core.forwarding.forward(packet, dst)
