from flex.core import core
from flex.network.network import Network

def launch():
    myself = core.myself.get_self_controller()
    backlog = core.config.get('module.network.backlog')
    core.register_component(Network, myself.get_address(), backlog)
