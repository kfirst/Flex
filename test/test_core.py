'''
Created on 2013-4-6

@author: kfirst
'''

from flex.core import core
core.start()
logger = core.get_logger()
logger.warning('test')
print core.network._myself
