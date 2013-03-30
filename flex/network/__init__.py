from flex.network.network import Network
from flex.core import core
from flex.model.device import Controller

def launch():
    config = core.config
    my_id = config.get('topology.my_id')
    address = config.get('module.network.address')
    backlog = config.get('module.network.backlog')
    core.register_component(Network, Controller(my_id, tuple(address)), backlog)
