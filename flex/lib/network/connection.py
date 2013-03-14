'''
Created on 2013-3-14

@author: kfirst
'''

class Connection(object):

    def __init__(self, sock, address, connection_handler):
        self._sock = sock
        self._address = address
        self._handler = connection_handler
        connection_handler.set_connection(self)

    def get_sock(self):
        return self._sock

    def get_address(self):
        return self._address

    def get_fileno(self):
        return self._sock.fileno()

    def handle(self, event):
        return self._handler.handle(event)

    def send(self, data):
        return self._handler.send(data)

    def recv(self, size = 1024):
        return self._sock.recv(size)

    def close(self):
        self._sock.close()
