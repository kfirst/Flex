# encoding: utf-8
'''
各种事件的定义
Created on 2013-3-30

@author: kfirst
'''

class NeighborControllerUpEvent(object):
    '''
    邻居Controller启动事件，在和邻居Controller建立连接并握手后发生
    '''
    def __init__(self, controller):
        self.controller = controller
