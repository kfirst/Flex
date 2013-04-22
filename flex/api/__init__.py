from flex.core import core
from flex.api.api import Api

def launch():
    myself = core.myself.get_self_controller()
    core.register_component(Api, myself)
