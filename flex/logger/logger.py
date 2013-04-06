# encoding: utf-8
'''
Created on 2013-3-19

@author: kfirst
'''

import inspect
import logging
import os
from flex.base.module import Module

_flexpath = inspect.stack()[0][1]
_flexpath = _flexpath[0:_flexpath.rindex(os.sep)]
_ext_flexpath = _flexpath[0:_flexpath.rindex(os.sep)]
_ext_flexpath = os.path.dirname(_ext_flexpath) + os.sep


class Logger(Module):

    def __init__(self, level, handlers):
        logger = logging.getLogger()
        logger.setLevel(level)
        for handler in handlers:
            logger.addHandler(handler)

    def get_logger (self, name = None, moreFrames = 0):
        if name is None:
            name = inspect.stack()[1 + moreFrames][1]
            if name.endswith('.py'):
                name = name[0:-3]
            elif name.endswith('.pyc'):
                name = name[0:-4]
            if name.endswith(".__init__"):
                name = name[0:-9]
            if name.startswith(_ext_flexpath):
                name = name[len(_ext_flexpath):]
            name = name.replace(os.sep, '.')
        logger = logging.getLogger(name)
        return logger

    def get_level(self):
        return self._level
