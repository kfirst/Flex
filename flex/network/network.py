# encoding: utf-8
'''

@author: kfirst
'''

import select
import base64
import threading
from flex.base.handler import ConnectionHandler, DataHandler
from flex.base.module import Module
from flex.base.exception import ConnectFailException
from flex.network.connection import Connection
from flex.core import core
import Queue

logger = core.get_logger()

class Network(Module):
    '''
    socket监听和发送
    '''

    EOL = b'#'

    def __init__(self, address, backlog):
        self._address = address
        self._backlog = backlog
        self._run = 1
        self._data_handler = EmptyDataHandler()

        # fd => connection
        self._in_connections = {}
        # fd => connection_handler
        self._in_handlers = {}
        # address => connection
        self._out_connections = {}

        self._epoll = select.epoll()

    def register_data_handler(self, data_handler):
        self._data_handler = data_handler

    def send(self, address, data):
        while 1:
            connection = self._get_out_connection(address)
            if not connection:
                return False
            data = '%s%s' % (base64.b64encode(data), self.EOL)
            try:
                writen = connection.send(data)
                break
            except Exception:
                self._remove_out_connection(address)
        return True

    def _get_out_connection(self, address):
        try:
            connection = self._out_connections[address]
        except KeyError:
            try:
                connection = Connection.get_client(address)
                self._out_connections[address] = connection
            except ConnectFailException, e:
                logger.warning(e)
                return False
        return connection

    def _remove_out_connection(self, address):
        connection = self._out_connections.pop(address)
        connection.close()

    def _accept_in_connection(self, connection):
        connection = connection.accept()
        fd = connection.get_fileno()
        self._in_connections[fd] = connection
        self._in_handlers[fd] = ClientHandler(connection, self)
        self._epoll.register(fd, select.EPOLLIN)

    def _remove_in_connection(self, connection):
        fd = connection.get_fileno()
        del self._in_connections[fd]
        del self._in_handlers[fd]
        self._epoll.unregister(fd)
        connection.close()

    def _handle_data(self, data):
        self._data_handler.handle(data)

    def _schedule(self):
        while self._run:
            events = self._epoll.poll(-1)
            for fd, event in events:
                try:
                    self._in_handlers[fd].handle(event)
                except:
                    pass

    def start(self):
        self._start_server()
        self._start_thread()

    def _start_server(self):
        server = Connection.get_server(self._address, self._backlog)
        fd = server.get_fileno()
        self._in_connections[fd] = server
        self._in_handlers[fd] = ServerHandler(server, self)
        self._epoll.register(fd, select.EPOLLIN)

    def _start_thread(self):
        thread = threading.Thread(target = self._schedule)
        thread.setDaemon(True)
        thread.start()

    def terminate(self):
        self._run = 0
        for fd, connection in self._in_connections.items():
            connection.close()
        for fd, connection in self._out_connections.items():
            connection.close()
        self._epoll.close()


class EmptyDataHandler(DataHandler):

    def handle(self, data):
        pass


class ServerHandler(ConnectionHandler):

    def __init__(self, connection, network):
        self._connection = connection
        self._network = network

    def handle(self, event):
        self._network._accept_in_connection(self._connection)


class ClientHandler(ConnectionHandler):

    EOL = Network.EOL
    EOL_LENGTH = len(EOL)

    def __init__(self, connection, network):
        self._connection = connection
        self._network = network
        self._receive_buffer = b''
        self._send_buffer = Queue.Queue()
        self._current_to_send = b''

    def handle(self, event):
        if event & select.EPOLLHUP:
            self._network._remove_in_connection(self._connection)
        elif event & select.EPOLLIN:
            data = self._connection.recv()
            if data:
                self._receive_buffer += data
                length = len(data) + ClientHandler.EOL_LENGTH
                try:
                    while 1:
                        index = self._receive_buffer.index(ClientHandler.EOL, -length)
                        data = base64.b64decode(self._receive_buffer[0:index])
                        self._receive_buffer = self._receive_buffer[index + ClientHandler.EOL_LENGTH:]
                        self._network._handle_data(data)
                except ValueError:
                    pass
            else:
                self._network._remove_in_connection(self._connection)
