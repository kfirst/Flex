from flex.core import core
from flex.control_packet_forwarding.control_packet_forwarding import ControlPacketForwarding

def launch():
    cpf = ControlPacketForwarding()

    core.register_object('control_packet_forwarding', cpf)
