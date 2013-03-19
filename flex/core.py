# encoding: utf-8
'''
Created on 2013-3-19

@author: kfirst
'''

import flex
import inspect
import logging
import os

_path = inspect.stack()[0][1]
_ext_path = _path[0:_path.rindex(os.sep)]
_path = os.path.dirname(_path) + os.sep
_ext_path = os.path.dirname(_ext_path) + os.sep

def register_component(component_class, *args, **kw):
    name = component_class.__name__
    obj = component_class(*args, **kw)
    setattr(flex.core, name, obj)

def getLogger (name = None, moreFrames = 0):
    if name is None:
        name = inspect.stack()[1 + moreFrames][1]
        if name.endswith('.py'):
            name = name[0:-3]
        elif name.endswith('.pyc'):
            name = name[0:-4]
        if name.endswith(".__init__"):
            name = name[0:-9]
        if name.startswith(_path):
            name = name[len(_path):]
        elif name.startswith(_ext_path):
            name = name[len(_ext_path):]
        name = name.replace(os.sep, '.')
    return logging.getLogger(name)


class Core(object):

    def __init__(self):
        pass

