# encoding: utf-8
'''
各种事件的定义
Created on 2013-3-30

@author: kfirst
'''
from flex.lib.util import object_to_string

class BaseEvent(object):

    def __repr__(self):
        return object_to_string(self)


class NeighborControllerUpEvent(BaseEvent):
    '''
    邻居Controller启动事件，在和邻居Controller建立连接并握手后发生
    '''
    def __init__(self, controller, relation):
        self.controller = controller
        self.relation = relation

    def __repr__(self):
        return object_to_string(self, controller = self.controller)


class FlexUpEvent(BaseEvent):
    '''
    Flex启动完毕事件
    '''
    def __init__(self):
        pass
