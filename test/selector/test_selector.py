'''
Created on 2013-4-8

@author: kfirst
'''

from flex.core import core

core.set_config_path('../config')
core.start()
selector = core.selector

values = set([1, 3, 5, 7, 9, 11, 13, 15])

from flex.selector.selector import Selector
print selector.select(Selector.CONTROLLER, values)
print selector.select(Selector.MODULE, values)
