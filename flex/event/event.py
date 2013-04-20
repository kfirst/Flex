# encoding: utf-8
'''
Created on 2013-3-30

@author: kfirst
'''

from flex.base.module import Module
from flex.core import core

logger = core.get_logger()

class Event(Module):
    '''
    事件模块，用于产生事件，并调用相应的事件处理程序    
    '''

    def __init__(self):
        self._handlers = {}

    '''
    注册事件处理程序。任何对某种事件感兴趣的模块，都可以使用该方法注册事件处理程序
    '''
    def register_handler(self, event_class, event_handler):
        try:
            self._handlers[event_class.__name__].append(event_handler)
        except KeyError:
            self._handlers[event_class.__name__] = [event_handler]

    '''
    引发某个事件。任何模块可以通过该方法引发某个事件，相应的事件处理程序的handle方法就会被调用
    '''
    def happen(self, event):
        try:
            name = event.__class__.__name__
            logger.debug(str(event) + ' happened')
            handlers = self._handlers[name]
            for handler in handlers:
                handler.handle_event(event)
        except KeyError:
            pass
