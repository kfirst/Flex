'''
Created on 2013-3-13

@author: kfirst
'''

class SocketPool(object):

    def __init__(self):
        self.__pool = {}

    def get_client(self, address):
        try:
            return self.__pool[address]
        except KeyError:
            return False

    def add_socket(self, address, sock):
        self.__pool[address] = sock

    def __del__(self):
        for address in self.__pool:
            try:
                self.__pool[address].close()
            except Exception, e:
                print e
