'''
Created on 2013-4-6

@author: kfirst
'''

from flex.core import core
core.set_config_path('config')
core.start()
logger = core.get_logger()
logger.warning('test')
print core.myself.get_self_type()
