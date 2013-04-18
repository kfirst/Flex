from flex.core import core
from flex.control_packet_forwarding.control_packet_forwarding import ControlPacketForwarding

def launch():
    core.register_component(ControlPacketForwarding)
