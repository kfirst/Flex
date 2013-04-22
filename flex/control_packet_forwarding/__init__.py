from flex.core import core
from flex.control_packet_forwarding.control_packet_forwarding import ControlPacketForwarding

def launch():
    myself = core.myself.get_self_controller()
    algorithms = core.config.get('module.control_packet_forwarding.algorithms')
    core.register_component(ControlPacketForwarding, myself, algorithms)
