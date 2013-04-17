from flex.core import core
from flex.forwarding.forwarding import Forwarding

def launch():
    myself = core.myself.get_self_controller()
    core.register_component(Forwarding, myself)
