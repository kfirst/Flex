'''
Created on 2013-4-6

@author: kfirst
'''
from flex.base.module import Module

class Myself(Module):

    POX = 'pox'
    FLEX = 'flex'

    def __init__(self, controller, controller_type):
        self._myself = controller
        self._type = controller_type

    def get_self_controller(self):
        return self._myself

    def get_self_type(self):
        return self._type
