'''
Created on 2013-4-6

@author: kfirst
'''

from flex.core import core
import time
from flex.base.handler import StorageHandler

class testListen(StorageHandler):

    def handle_storage(self, key, value, domain, type):
        print key
        print value


core.set_config_path('config')
core.start()
logger = core.get_logger()
logger.warning('test')
core.myself.get_self_controller()
print core.globalStorage.set('bbbbbbbbb', 12323)
print core.globalStorage.get('bbbbbbbbb')
# core.globalStorage.listen_domain(testListen(), 'default', listen_myself = True)
# core.globalStorage.sadd_multi('bb', ([1, 2], 'a'))
time.sleep(1)
