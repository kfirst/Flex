'''
Created on 2013-4-6

@author: kfirst
'''

from flex.core import core
import time
core.set_config_path('config')
core.start()
logger = core.get_logger()
logger.warning('test')
print core.myself.get_self_controller()
print core.globalStorage.sadd_multi('bb', ([1, 2], 'a'))
print core.globalStorage.sget('b')
time.sleep(1)
