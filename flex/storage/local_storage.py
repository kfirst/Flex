'''
Created on 2013-5-13

@author: kfirst
'''

from flex.base.module import Module


class LocalStorage(Module):

    def __init__(self):
        self._values = {}
        self._sets = {}

    def _make_name(self, key, domain):
        return '%s:%s' % (domain, key)

    def get(self, key, domain = 'default'):
        return self._values.get(self._make_name(key, domain))

    def set(self, key, value, domain = 'default'):
        self._values[self._make_name(key, domain)] = value

    def delete(self, key, domain = 'default'):
        del self._values[self._make_name(key, domain)]

    def sget(self, key, domain = 'default'):
        return self._sets.get(self._make_name(key, domain))

    def sadd(self, key, value, domain = 'default'):
        name = self._make_name(key, domain)
        try:
            self._sets[name].add(value)
        except KeyError:
            self._sets[name] = set([value])

    def sremove(self, key, value, domain = 'default'):
        name = self._make_name(key, domain)
        self._sets[name].discard(value)

    def sadd_multi(self, key, values, domain = 'default'):
        for value in values:
            self.sadd(key, value)

    def listen(self, key, storage_handler, listen_myself = False):
        pass
