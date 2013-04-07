from flex.core import core
from flex.pox.pox_app import PoxApp

def launch():
    import os, sys
    pox_path = core.config.get('module.pox.pox_path')
    sys.path.append(os.path.abspath(pox_path))

    pox_config = core.config.get('module.pox.pox_command_line')
    myself = core.myself.get_self_controller()
    pox_app = PoxApp(myself, pox_config)
    core.register_object('pox', pox_app)
