# encoding: utf-8
'''
socket生成器

@author: kfirst
'''

import socket
from flex.lib.network.connection import Connection
from flex.base.exception import ConnectFailException

class ConnectionGenerator(object):

    def get_client(self, address, connection_handler):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            client.connect(address)
            client.setblocking(False)
            return Connection(client, address, connection_handler)
        except Exception, e:
            raise ConnectFailException('Can not connect to ' + str(address) + ', because of ' + str(e))

    def get_server(self, address, backlog, connection_handler):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            server.bind(address)
            server.listen(backlog)
            server.setblocking(False)
            return Connection(server, address, connection_handler)
        except Exception, e:
            raise ConnectFailException('Can not start server at ' + str(address) + ', because of ' + str(e))

    def accept(self, connection, connection_handler):
        sock, address = connection.get_sock().accept()
        sock.setblocking(False)
        return Connection(sock, address, connection_handler)
