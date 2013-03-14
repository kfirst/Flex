# encoding: utf-8
'''
Created on 2013-3-13

@author: kfirst
'''

import select
from flex.lib.network.connection_pool import ConnectionPool
from flex.lib.network.connection_generator import ConnectionGenerator
from flex.lib.network.connection_monitor import ConnectionMonitor
from flex.base.handler import ConnectionHandler

class Network(object):

    def __init__(self, address, backlog, data_handler):
        self._connection_pool = ConnectionPool()
        self._generator = ConnectionGenerator()
        self._monitor = ConnectionMonitor()
        self._handler = data_handler
        server = self._generator.get_server(address, backlog, ServerHandler(self))
        self._connection_pool.add(address, server);
        self._monitor.add(server);

    def send(self, address, data):
        connection = self._connection_pool.get(address)
        if not connection:
            connection = self._generator.get_client(address, ClientHandler(self, self._handler))
            self._connection_pool.add(connection.get_address(), connection)
            self._monitor.add(connection)
        connection.send(data)

    def schedule(self, timeout = 0):
        self._monitor.schedule(timeout)

    def _accept_connection(self, connection, event):
        connection = self._generator.accept(connection, ClientHandler(self, self._handler))
        self._connection_pool.add(connection.get_address(), connection)
        self._monitor.add(connection)

    def _remove_connection(self, connection):
        self._connection_pool.remove(connection)
        self._monitor.remove(connection)
        connection.close()


class ServerHandler(ConnectionHandler):

    def __init__(self, network):
        self._network = network

    def handle(self, event):
        self._network._accept_connection(self._connection, event)


class ClientHandler(ConnectionHandler):

    EOL = b'\r\n'
    EOL_LENGTH = len(EOL)

    def __init__(self, network, data_listener):
        self._network = network
        self._handler = data_listener
        self._request = ''
        self._response = []

    def handle(self, event):
        if event & select.EPOLLIN:
            data = self._connection.recv()
            self._request += data
            try:
                while(True):
                    index = self._request.index(ClientHandler.EOL, -len(data) - ClientHandler.EOL_LENGTH)
                    self._handler.handle(self._request[0:index])
                    self._request = self._request[index + ClientHandler.EOL_LENGTH:]
            except ValueError:
                pass
        elif event & select.EPOLLOUT:
            if self._response:
                writen = self._connection.get_sock().send(self._response[0])
                if len(self._response[0]) == writen:
                    del self._response[0]
                else:
                    self._response[0] = self._response[0][writen:]
        elif event & select.EPOLLHUP:
            self._network._remove_connection(self._connection)

    def send(self, data):
        self._response.append(data + ClientHandler.EOL)


if __name__ == '__main__':
    import time
    class PrintHandler:
        def handle(self, data):
            print 'received:' + data

    net1 = Network(('127.0.0.1', 22222), 2, PrintHandler())
    net2 = Network(('127.0.0.1', 22223), 2, PrintHandler())
    for i in range(1, 3):
        net2.send(('127.0.0.1', 22222), 'I\'m net2')
        net1.send(('127.0.0.1', 22223), 'I\'m net1')
        net1.schedule(0)
        net2.schedule(0)
        time.sleep(1)
    net1.schedule(0)
    net2.schedule(0)
