'''
Created on 2013-4-8

@author: kfirst
'''
from flex.base.module import Module
from flex.core import core
import random

logger = core.get_logger()

class Selector(Module):

    CONTROLLER = 'controller'
    MODULE = 'module'

    def __init__(self):
        self._algorithms = {}
        self._parameters = {}

    def register_algorithm(self, value_type, algorithm, argv):
        try:
            self._algorithms[value_type] = getattr(self, algorithm)
            self._parameters[value_type] = argv
        except AttributeError:
            logger.error('Algorithm [' + algorithm + '] does not defined')

    def select(self, value_type, values):
        try:
            parameter = self._parameters[value_type]
            return self._algorithms[value_type](values, *parameter)
        except KeyError:
            return self.sample(values)

    def sample(self, values, size = 1):
        return random.sample(values, size)

    def all(self, values):
        return values
