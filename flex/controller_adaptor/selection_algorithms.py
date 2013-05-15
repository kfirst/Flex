'''
Created on 2013-5-14

@author: kfirst
'''
import random
from flex.core import core

class SelectionAlgorithms(object):

    @classmethod
    def shortest_path(self, controllers):
        if len(controllers) < 2:
            return controllers
        ret = None
        shorest = None
        for controller in controllers:
            distance = core.routing.get_distance(controller)
            if shorest == None or distance < shorest:
                shorest = distance
                ret = controller
        return [ret]

    @classmethod
    def first(self, controllers):
        return [controllers[0]]

    @classmethod
    def sample(self, controllers, size):
        return random.sample(controllers, min(len(controllers), size))
