'''
Created on 2013-4-6

@author: kfirst
'''

from flex.base.module import Module
from flex.core import core as flex_core
from flex.model.packet import Packet
from flex.pox.flex_handlers import LocalHandler

logger = flex_core.get_logger()

class PoxApp(Module):

    def __init__(self, self_controller, pox_config):
        self._myself = self_controller
        self._config = pox_config

    def start(self):
        launch_pox(self._config, self)

        from flex.pox.switch_pool import SwitchPool
        from flex.pox.pox_handlers import TopologyHandler
        self._pool = SwitchPool()
        self._topo_handler = TopologyHandler(self._pool, self._myself)

        from flex.pox.flex_handlers import ConcernHandler
        flex_core.network.register_handler(Packet.LOCAL_CONCERN, ConcernHandler(self._myself))
        flex_core.network.register_handler(Packet.LOCAL_TO_POX, LocalHandler(self._pool))


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
