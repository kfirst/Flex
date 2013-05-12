from flex.core import core
from flex.concern_packet_forwarding.concern_packet_forwarding import ConcernPacketForwarding

def launch():
    myself = core.myself.get_self_controller()
    algorithms = core.config.get('module.control_packet_forwarding.algorithms')
    core.register_component(ConcernPacketForwarding, myself, algorithms)
