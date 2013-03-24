from flex.network.network import Network
from flex.core import core

def launch():
    config = core.config
    address = config.get('module.network.address')
    backlog = config.get('module.network.backlog')
    core.register_component(Network, address, backlog)
