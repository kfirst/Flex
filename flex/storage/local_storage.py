'''
Created on 2013-5-13

@author: kfirst
'''

from flex.base.module import Module


class LocalStorage(Module):

    def __init__(self):
        self._values = {}
        self._sets = {}

    def get(self, key):
        return self._values.get(key)

    def set(self, key, value):
        self._values[key] = value

    def sget(self, key):
        return self._sets.get(key)

    def sadd(self, key, value):
        try:
            self._sets[key].add(value)
        except KeyError:
            self._sets[key] = set([value])

    def sadd_multi(self, key, values):
        for value in values:
            self.sadd(key, value)

    def listen(self, key, storage_handler, listen_myself = False):
        pass
