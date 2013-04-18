# encoding: utf-8
'''
Created on 2013-4-6

@author: fzm
'''

from flex.core import core
from flex.base.handler import PacketHandler
from flex.model.packet import Packet, RegisterConcersContent
from flex.myself.myself import Myself

logger = core.get_logger()

class RegisterConcernsHandler(PacketHandler):
    '''
    处理收到的RegisterConcern报文，该报文的目的是告诉邻居，
    自己关心的报文是指定的switch产生的指定类型的control报文，
    以便在邻居收到相应switch产生的相应类型的control报文时，转发给自己。
    收到RegisterConcern报文后的处理流程如下：
    1. 读取报文的内容，更新自己的信息；
    2. 如果自己的信息有更新，将自己信息的更新部分（注意不是原报文中的全部信息，否则将不收敛）
    发给除原报文来源以外的peer和customer；
    
    TODO
    1. 当Controller Down时，清理自己的信息，否则在Down的Controller重启后将不能正常工作
    2. 当Switch Down时，清理自己的信息，否则在Down的Switch重启后将不能正常工作
    '''

    ALL_SWITCHES = RegisterConcersContent.ALL_SWITCHES

    def __init__(self, control_packet_forwarding):
        self._forwarding = control_packet_forwarding

    def __getattr__(self, name):
        return getattr(self._forwarding, name)

    def handle(self, packet):
        logger.debug('Receive an Register Concerns Packet:' + str(packet))
        controller = packet.content.controller
        types = packet.content.types
        concern_types = {}
        for concern_type, switches in types.items():
            added_switches = self._update_concern_types(concern_type, switches)
            self._update_controller_concerns(controller, concern_type, switches)
            if added_switches:
                concern_types[concern_type] = added_switches
        if concern_types:
            self._send_packet_to_neighbors(concern_types, controller)

    def _update_concern_types(self, concern_type, switches):
        return self._update_concerns(self.concern_types, concern_type, switches)

    def _update_controller_concerns(self, controller, concern_type, switches):
        try:
            concern_types = self.controller_concerns[controller]
            self._update_concerns(concern_types, concern_type, switches)
        except KeyError:
            if switches == self.ALL_SWITCHES:
                self.controller_concerns[controller] = {concern_type: self.ALL_SWITCHES}
            else:
                self.controller_concerns[controller] = {concern_type: set(switches)}

    def _update_concerns(self, concern_types, concern_type, switches):
        try:
            added_switches = concern_types[concern_type]
            if added_switches != self.ALL_SWITCHES:
                if switches == self.ALL_SWITCHES:
                    concern_types[concern_type] = self.ALL_SWITCHES
                else:
                    switches -= added_switches
                    added_switches.update(switches)
                return switches
        except KeyError:
            if switches == self.ALL_SWITCHES:
                concern_types[concern_type] = self.ALL_SWITCHES
            else:
                concern_types[concern_type] = set(switches)
            return switches
        return None

    def _send_packet_to_neighbors(self, concern_types, src):
        peer_controllers = core.topology.get_peers()
        peer_controllers.discard(src)
        customer_controllers = core.topology.get_customers()
        customer_controllers.discard(src)

        content = RegisterConcersContent(self.self_controller, concern_types)
        packet = Packet(Packet.REGISTER_CONCERN, content)

        for controller in peer_controllers:
            core.forwarding.forward(packet, controller)
        for controller in customer_controllers:
            core.forwarding.forward(packet, controller)

        if self.type == Myself.POX:
            packet.type = Packet.LOCAL_CONCERN
            core.forwarding.forward(packet)
