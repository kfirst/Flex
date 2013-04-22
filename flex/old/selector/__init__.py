from flex.core import core
from flex.selector.selector import Selector

def launch():
    algorithm = core.config.get('module.selector.algorithm')
    parameter = core.config.get('module.selector.parameter')
    core.register_component(Selector, algorithm, parameter)
