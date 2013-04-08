'''
Created on 2013-4-8

@author: kfirst
'''

from flex.core import core

core.set_config_path('../config')
core.start()
selector = core.selector

values = set([1, 2, 3, 4, 5])
print selector.select(values)
print selector.select(values)
