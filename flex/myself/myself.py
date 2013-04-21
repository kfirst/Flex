'''
Created on 2013-4-6

@author: kfirst
'''
from flex.base.module import Module
from flex.core import core

logger = core.get_logger()

class Myself(Module):

    POX = 'pox'
    FLEX = 'flex'

    def __init__(self, controller):
        self._myself = controller

    def start(self):
        logger.info('I am ' + str(self._myself))

    def get_self_controller(self):
        return self._myself
