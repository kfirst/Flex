'''
Created on 2013-3-30

@author: kfirst
'''

from flex.base.module import Module

class Event(Module):

    def __init__(self):
        self._handlers = {}

    def add_handler(self, event_class, event_handler):
        try:
            self._handlers[event_class.__name__].append(event_handler)
        except KeyError:
            self._handlers[event_class.__name__] = [event_handler]

    def happen(self, event):
        try:
            handlers = self._handlers[event.__class__.__name__]
            for handler in handlers:
                handler.handle(event)
        except KeyError:
            pass
