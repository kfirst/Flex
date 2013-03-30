'''
Created on 2013-3-14

@author: kfirst
'''

class ConnectionHandler(object):

    def set_connection(self, connection):
        self._connection = connection

    def handle(self, event):
        pass

    def send(self, data):
        pass


class DataHandler(object):

    def handle(self, address, data):
        pass


class PacketHandler(object):

    def handle(self, packet):
        pass


class EventHandler(object):

    def handle(self, event):
        pass
