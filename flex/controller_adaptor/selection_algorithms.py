'''
Created on 2013-5-14

@author: kfirst
'''
import random
from flex.core import core

class SelectionAlgorithms(object):

    @classmethod
    def shortest_path(cls, controllers):
        if len(controllers) < 2:
            return controllers
        ret = None
        shorest = None
        for controller in controllers:
            distance = core.routing.get_distance(controller)
            if shorest is None or distance < shorest:
                shorest = distance
                ret = controller
        return [ret]

    @classmethod
    def sample(cls, controllers, size):
        return random.sample(controllers, min(len(controllers), size))
