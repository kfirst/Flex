from flex.core import core
from flex.pox.pox_app import PoxApp

def launch():
    pox_config = core.config.get('module.pox.pox_command_line')
    myself = core.myself.get_self_controller()
    pox_app = PoxApp(myself, pox_config)
    core.register_object('pox', pox_app)
