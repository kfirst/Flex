#!/usr/bin/env python
'''
Created on 2013-4-7

@author: kfirst
'''

from flex.core import core
import sys
import time

try:
    config_path = sys.argv[1]
except IndexError:
    config_path = 'config'

core.set_config_path(config_path)
core.start()

logger = core.get_logger()
logger.info('Flex is up')

try:
    while True:
        time.sleep(10)
except:
    pass

logger.info('Terminating')
core.terminate()
logger.info('Terminated')
