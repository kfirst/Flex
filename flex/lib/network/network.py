'''
Created on 2013-3-13

@author: kfirst
'''
from flex.lib.network.socket_pool import SocketPool
from flex.lib.network.socket_generator import SocketGenerator
from flex.lib.network.socket_monitor import SocketMonitor

class Network(object):

    def __init__(self, address, backlog, socket_listener):
        self.__pool = SocketPool(self)
        self.__generator = SocketGenerator(self)
        self.__monitor = SocketMonitor(self)
        self.__socket_listener = socket_listener
        server = self.__generator.get_server(address, backlog)
        self.__pool.add_socket(address, server);
        self.__monitor.add_socket(server, self);

    def handle(self, sock):
        (sock, address) = sock.accept()
        sock.setblocking(False)
        self.__pool.add_socket(address, sock)
        self.__monitor.add_socket(sock, self.__socket_listener)
