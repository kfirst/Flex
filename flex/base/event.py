# encoding: utf-8
'''
各种事件的定义
Created on 2013-3-30

@author: kfirst
'''
from flex.lib.util import object_to_string

class BaseEvent(object):

    def __repr__(self):
        return self.__str__()


class NeighborControllerUpEvent(BaseEvent):
    '''
    邻居Controller启动事件，在和邻居Controller建立连接并握手后发生
    '''
    def __init__(self, controller):
        self.controller = controller

    def __str__(self):
        return object_to_string(self, controller = self.controller)
