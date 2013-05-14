'''
Created on 2013-4-6

@author: kfirst
'''

from flex.base.module import Module
from flex.core import core as flex_core
import time

logger = flex_core.get_logger()

class PoxApp(Module):

    def __init__(self, self_controller, pox_config):
        self._myself = self_controller
        self._config = pox_config

    def start(self):
        launch_pox(self._config, self)
        time.sleep(1)

        from flex.pox.managers import ConcernManager
        self.concern_manager = ConcernManager()
        from flex.pox.managers import ProcesserManager
        self.processer_manager = ProcesserManager()

    def register(self, concern_type, switch = None):
        self.concern_manager.add(concern_type, switch)

    def process(self, api_content):
        self.processer_manager.process(api_content)

    def terminate(self):
        terminate_pox()


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

def terminate_pox():
    from pox.core import core as pox_core
    pox_core.quit()

def launch():
    from pox.core import core as pox_core
    if not pox_core.hasComponent('pox_app'):
        pox_core.register('pox_app', pox_app)
        logger.debug('POX app registered')
