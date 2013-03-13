'''
socket生成器

@author: kfirst
'''

import socket

class SocketGenerator(object):

    def get_client(self, address):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            client.connect(address)
            return client
        except Exception, e:
            print e
            return False

    def get_server(self, address = '0.0.0.0', backlog = 100):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            server.bind(address)
            server.listen(backlog)
            server.setblocking(False)
            return server
        except Exception, e:
            print e
            return False
