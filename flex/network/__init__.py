from flex.network.network import Network
from flex.core import core
from flex.model.device import Controller

def launch():
    myself = core.myself.get_self_controller()
    backlog = core.config.get('module.network.backlog')
    core.register_component(Network, myself, backlog)
