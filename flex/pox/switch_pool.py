'''
Created on 2013-4-5

@author: kfirst
'''

class SwitchPool(object):

    def __init__(self):
        self._switches = {}

    def set(self, key, switch):
        self._switches[key] = switch

    def get(self, key):
        return self._switches[key]

    def remove(self, key):
        del self._switches[key]
