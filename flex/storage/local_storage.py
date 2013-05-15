'''
Created on 2013-5-13

@author: kfirst
'''

from flex.base.module import Module


class LocalStorage(Module):

    SET = 1
    SADD = 2
    SADD_MULTI = 3
    SREMOVE = 4
    DELETE = 5

    def __init__(self):
        self._values = {}
        self._sets = {}
        self._listen_name = {}
        self._listen_domain = {}

    def _make_name(self, key, domain):
        return '%s:%s' % (domain, key)

    def get(self, key, domain = 'default'):
        return self._values.get(self._make_name(key, domain))

    def set(self, key, value, domain = 'default'):
        self._values[self._make_name(key, domain)] = value
        self._notify(key, value, domain, self.SET)

    def delete(self, key, domain = 'default'):
        del self._values[self._make_name(key, domain)]
        self._notify(key, None, domain, self.DELETE)

    def sget(self, key, domain = 'default'):
        value = self._sets.get(self._make_name(key, domain))
        if value:
            return value
        return set()

    def sadd(self, key, value, domain = 'default'):
        name = self._make_name(key, domain)
        try:
            self._sets[name].add(value)
        except KeyError:
            self._sets[name] = set([value])
        self._notify(key, value, domain, self.SADD)

    def sremove(self, key, value, domain = 'default'):
        name = self._make_name(key, domain)
        self._sets[name].discard(value)
        self._notify(key, value, domain, self.SREMOVE)

    def sadd_multi(self, key, values, domain = 'default'):
        for value in values:
            self.sadd(key, value)
        self._notify(key, values, domain, self.SADD_MULTI)

    def listen_key(self, storage_handler, key, domain = 'default', listen_myself = False):
        if listen_myself:
            try:
                self._listen_name[self._make_name(key, domain)].add(storage_handler)
            except KeyError:
                self._listen_name[self._make_name(key, domain)] = set([storage_handler])

    def _notify(self, key, value, domain, type):
        self._notify_domain(key, value, domain, type)
        self._notify_key(key, value, domain, type)

    def _notify_domain(self, key, value, domain, type):
        try:
            listeners = self._listen_domain[domain]
            for listener in listeners:
                listener.handle_storage(key, value, domain, type)
        except KeyError:
            pass

    def _notify_key(self, key, value, domain, type):
        try:
            listeners = self._listen_name[self._make_name(key, domain)]
            for listener in listeners:
                listener.handle_storage(key, value, domain, type)
        except KeyError:
            pass

    def listen_domain(self, storage_handler, domain, listen_myself = False):
        if listen_myself:
            try:
                self._listen_domain[domain].add(storage_handler)
            except KeyError:
                self._listen_domain[domain] = set([storage_handler])
