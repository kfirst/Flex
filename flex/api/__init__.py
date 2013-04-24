from flex.core import core
from flex.api.api import Api

def launch():
    import os, sys
    pox_path = core.config.get('module.pox.pox_path')
    sys.path.append(os.path.abspath(pox_path))

    print os.path.abspath(pox_path)

    myself = core.myself.get_self_controller()
    core.register_component(Api, myself)
