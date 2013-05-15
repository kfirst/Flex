'''
Created on 2013-5-15

@author: kfirst
'''

from flex.model.action import OutputAction
from flex.base.module import Module


class ActionApi(Module):

    def output_action(self, port):
        return OutputAction(port)
