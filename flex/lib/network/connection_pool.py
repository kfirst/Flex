# encoding: utf-8
'''
Created on 2013-3-13

@author: kfirst
'''

class ConnectionPool(object):

    def __init__(self):
        self._connection_pool = {}
        self._address_pool = {}

    def get(self, address):
        try:
            return self._connection_pool[address]
        except KeyError:
            return False

    def add(self, address, connection):
        self._connection_pool[address] = connection
        self._address_pool[connection] = address

    def remove(self, connection):
        address = self._address_pool.pop(connection)
        del self._connection_pool[address]
