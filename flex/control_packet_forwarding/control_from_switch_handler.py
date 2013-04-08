'''
Created on 2013-4-6

@author: fzm
'''
from flex.core import core
from flex.base.handler import PacketHandler

logger = core.get_logger()

class Control_From_Switch_Handler(PacketHandler):
    def __init__(self, control_packet_forwarding):
        self._control = control_packet_forwarding

    def __getattr__(self, name):
        return getattr(self._control, name)

    def handle(self, packet):
        target_controllers = core.selector.controller(self.type_controller[type])
        for controller in target_controllers:
            if controller.get_id == self.self_id:
                self.target_is_self(packet)
            else:
                self.target_is_others(packet, controller)

    def target_is_self(self, packet):
        target_modules = core.selector.module(self.type_module[type])
        for module in target_modules:
            # module.handle(packet)
            pass

    def target_is_others(self, packet, controller):
        targrt_controller = core.topology.next_hop_of_controller(controller)
        core.network.send(targrt_controller, packet)

