from flex.core import core
from flex.network.network import Network

def launch():
    myself = core.myself.get_self_controller()
    backlog = core.config.get('module.network.backlog')
    buffer_size = core.config.get('module.network.buffer_size', 1024)
    core.register_component(Network, myself.get_address(), backlog, buffer_size)
