from flex.core import core
from flex.selector.selector import Selector

def launch():
    algorithms = core.config.get('module.selector')
    selector = Selector()
    for value_type in algorithms:
        algorithm_info = algorithms[value_type]
        algorithm = algorithm_info[0]
        parameter = algorithm_info[1:]
        selector.register_algorithm(value_type, algorithm, parameter)
    core.register_object('selector', selector)
