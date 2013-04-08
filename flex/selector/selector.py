'''
Created on 2013-4-8

@author: kfirst
'''
from flex.base.module import Module
from flex.core import core
import random

logger = core.get_logger()

class Selector(Module):

    def __init__(self, algorithm, argv):
        try:
            self._algorithm = getattr(self, algorithm)
            self._parameter = argv
        except AttributeError:
            logger.error('Algorithm [' + algorithm + '] does not defined')
            self._algorithm = self.sample

    def select(self, values):
        parameter = self._parameter
        return self._algorithm(values, *parameter)

    def sample(self, values, size = 1):
        return random.sample(values, min(len(values), size))

    def all(self, values):
        return values
