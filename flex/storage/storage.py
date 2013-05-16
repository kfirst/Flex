'''
Created on 2013-5-13

@author: kfirst
'''

from flex.base.module import Module


class Storage(Module):

    SET = 1
    SADD = 2
    SADD_MULTI = 3
    SREMOVE = 4
    DELETE = 5


    def get(self, key, domain = 'default'):
        pass

    def set(self, key, value, domain = 'default'):
        pass

    def delete(self, key, domain = 'default'):
        pass

    def sget(self, key, domain = 'default'):
        pass

    def sadd(self, key, value, domain = 'default'):
        pass

    def sremove(self, key, value, domain = 'default'):
        pass

    def sadd_multi(self, key, values, domain = 'default'):
        pass

    def listen_key(self, storage_handler, key, domain = 'default', listen_myself = False):
        pass

    def listen_domain(self, storage_handler, domain, listen_myself = False):
        pass
