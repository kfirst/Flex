'''
Created on 2013-5-12

@author: kfirst
'''

import pylibmc
from flex.base.module import Module


class Storage(Module):

    def __init__(self, servers):
        self._storage = pylibmc.Client(servers, binary = True,
                                behaviors = {'tcp_nodelay': True, 'ketama': True})

    def set(self, key, value, domain = ''):
        if not key:
            raise Exception('key can not be empty!')
        return self._storage.set(str('%s_%s' % (domain, key)), value)

    def get(self, key, default = None, domain = ''):
        if not key:
            raise Exception('key can not be empty!')
        value = self._storage.get(str('%s_%s' % (domain, key)))
        if value == None:
            value = default
        return value
