'''
Created on 2013-3-14

@author: kfirst
'''

import socket
from flex.base.exception import ConnectFailException

class Connection(object):

    SERVER = 0
    CLIENT = 1

    @staticmethod
    def get_client(address):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            client.connect(address)
            client.setblocking(False)
            return Connection(client, address, Connection.CLIENT)
        except Exception, e:
            raise ConnectFailException('Can not connect to ' + str(address) + ', because of ' + str(e))

    @staticmethod
    def get_server(address, backlog):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            server.bind(address)
            server.listen(backlog)
            server.setblocking(False)
            return Connection(server, address, Connection.SERVER)
        except Exception, e:
            raise ConnectFailException('Can not start server at ' + str(address) + ', because of ' + str(e))


    def __init__(self, sock, address, connection_type):
        self._sock = sock
        self._address = address
        self._type = connection_type

    def accept(self):
        sock, address = self._sock.accept()
        sock.setblocking(False)
        return Connection(sock, address, Connection.CLIENT)

    def get_type(self):
        return self._type

    def get_address(self):
        return self._address

    def get_fileno(self):
        return self._sock.fileno()

    def send(self, data):
        return self._sock.send(data)

    def recv(self, size = 1024):
        return self._sock.recv(size)

    def close(self):
        self._sock.close()
