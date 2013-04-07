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

while True:
    time.sleep(10)
