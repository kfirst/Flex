from flex.core import core
from flex.controller_adaptor.controller_adaptor import ControllerAdaptor

def launch():
    config = core.config.get('module.controller_adaptor')
    core.register_component(ControllerAdaptor, config['app'], config['algorithms'])
