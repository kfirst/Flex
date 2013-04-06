from flex.core import core
from flex.model.device import Controller
from flex.myself.myself import Myself

def launch():
    config = core.config
    my_id = config.get('topology.my_id')
    self_info = config.get('topology.controllers.' + my_id)
    self_controller = Controller(my_id, tuple(self_info['address']))
    self_type = self_info['type']
    core.register_component(Myself, self_controller, self_type)
