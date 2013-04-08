'''
Created on 2013-4-6

@author: kfirst
'''

from flex.base.module import Module
from flex.core import core as flex_core
from flex.model.packet import ControlPacketContent as control

logger = flex_core.get_logger()

class PoxApp(Module):

    def __init__(self, self_controller, pox_config):
        self._myself = self_controller
        self._config = pox_config

    def start(self):
        launch_pox(self._config, self)

        from flex.pox.switch_pool import SwitchPool
        from flex.pox.pox_handlers import *
        self._pool = SwitchPool()
        self._topo_handler = TopologyHandler(self._pool, self._myself)
        self._handlers = {}
        self._handlers_name = {
            control.CONNECTION_UP: ConnectionUpHandler,
            control.CONNECTION_DOWN: ConnectionDownHandler
        }

    def handle_packet(self, control_type):
        if control_type not in self._handlers:
            try:
                handler_class = self._handlers_name[control_type]
            except KeyError:
                logger.error('No handler for type [' + type + ']')
                return
            self._handlers[control_type] = handler_class(self._myself)


pox_app = None

def launch_pox(config, app):
    global pox_app
    pox_app = app

    argv = config.split()
    argv.append('flex.pox.pox_app')
    pre = []
    while len(argv):
        if argv[0].startswith("-"):
            pre.append(argv.pop(0))
        else:
            break
    argv = pre + "py --disable".split() + argv

    from pox.boot import _do_launch, _post_startup
    from pox.core import core as pox_core
    if _do_launch(argv):
        _post_startup()
        pox_core.goUp()


def launch():
    from pox.core import core as pox_core
    pox_core.register('pox_app', pox_app)
    logger.debug('POX app registered')
