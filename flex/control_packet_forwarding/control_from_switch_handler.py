'''
Created on 2013-4-6

@author: fzm
'''
from flex.core import core
from flex.base.handler import PacketHandler
from flex.model.packet import  Packet

logger = core.get_logger()

class Control_From_Switch_Handler(PacketHandler):
    def __init__(self, control_packet_forwarding):
        self._control = control_packet_forwarding

    def __getattr__(self, name):
        return getattr(self._control, name)

    def handle(self, packet):
        packet_type = packet.content.types
        try:
            target_controllers = core.selector.select(self.type_controller[packet_type])
            print target_controllers
        except KeyError:
            logger.warning('Control Packet of (' + str(packet_type) + ') type is not found!')
        for controller in target_controllers:
            if controller.get_id == self.self_id:
                self.target_is_self(packet)
            else:
                self.target_is_others(packet, controller)

    def target_is_self(self, packet):
        packet.type = Packet.LOCAL_TO_API
        core.network.send(self.self_controller, packet)

    def target_is_others(self, packet, controller):
        targrt_controller = core.topology.next_hop_of_controller(controller)
        core.network.send(targrt_controller, packet)

