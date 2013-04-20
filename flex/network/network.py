# encoding: utf-8
'''

@author: kfirst
'''

import select
import base64
import threading
from flex.base.handler import ConnectionHandler
from flex.base.module import Module
from flex.base.exception import ConnectFailException
from flex.network.connection import Connection
from flex.core import core

logger = core.get_logger()

class Network(Module):
    '''
    socket监听和发送
    '''

    def __init__(self, address, backlog):
        self._address = address
        self._backlog = backlog
        self._run = True
        # address => connection
        self._connections = {}
        # address => fd
        self._connection_fds = {}
        # fd => connection_handler
        self._connection_handlers = {}
        self._epoll = select.epoll()

    def register_data_handler(self, data_handler):
        self._data_handler = data_handler

    def send(self, address, data):
        if address not in self._connection_fds:
            try:
                self._add(address)
            except ConnectFailException, e:
                logger.warning(e)
                return False
        fd = self._connection_fds[address]
        handler = self._connection_handlers[fd]
        handler.send(data)
        return True

    def _add(self, address):
        connection = Connection.get_client(address)
        self._add_connection(connection)

    def _accept_connection(self, connection):
        connection = connection.accept()
        self._add_connection(connection)

    def _add_connection(self, connection):
        address = connection.get_address()
        fd = connection.get_fileno()
        self._connections[address] = connection
        self._connection_fds[address] = fd
        self._connection_handlers[fd] = ClientHandler(connection, self)
        self._epoll.register(fd, select.EPOLLIN | select.EPOLLOUT)

    def _remove_connection(self, connection):
        address = connection.get_address()
        del self._connections[address]
        del self._connection_fds[address]
        fd = connection.get_fileno()
        del self._connection_handlers[fd]
        self._epoll.unregister(fd)
        connection.close()

    def _handle_data(self, data):
        try:
            self._data_handler.handle(data)
        except AttributeError:
            pass

    def _schedule(self):
        while self._run:
            events = self._epoll.poll(-1)
            for fd, event in events:
                try:
                    self._connection_handlers[fd].handle(event)
                except:
                    pass
        self._epoll.close()

    def start(self):
        self._start_server()
        self._start_thread()

    def _start_server(self):
        self._server = Connection.get_server(self._address, self._backlog)
        fd = self._server.get_fileno()
        self._connection_handlers[fd] = ServerHandler(self._server, self)
        self._epoll.register(fd, select.EPOLLIN | select.EPOLLOUT)

    def _start_thread(self):
        thread = threading.Thread(target = self._schedule)
        thread.setDaemon(True)
        thread.start()

    def terminate(self):
        self._epoll.unregister(self._server.get_fileno())
        for address in self._connection_fds:
            fd = self._connection_fds[address]
            self._epoll.unregister(fd)
            self._connections[address].close()
        self._server.close()
        self._run = False


class ServerHandler(ConnectionHandler):

    def __init__(self, connection, network):
        self._connection = connection
        self._network = network

    def handle(self, event):
        self._network._accept_connection(self._connection)


class ClientHandler(ConnectionHandler):

    EOL = b'\n'
    EOL_LENGTH = len(EOL)

    def __init__(self, connection, network):
        self._connection = connection
        self._network = network
        self._receive_buffer = b''
        self._send_buffer = []

    def handle(self, event):
        if event & select.EPOLLHUP:
            self._network._remove_connection(self._connection)
        elif event & select.EPOLLIN:
            data = self._connection.recv()
            self._receive_buffer += data
            try:
                while(True):
                    index = self._receive_buffer.index(ClientHandler.EOL, -len(data) - ClientHandler.EOL_LENGTH)
                    data = self._decode_data(self._receive_buffer[0:index])
                    self._network._handle_data(data)
                    self._receive_buffer = self._receive_buffer[index + ClientHandler.EOL_LENGTH:]
            except ValueError:
                pass
        elif event & select.EPOLLOUT:
            if self._send_buffer:
                writen = self._connection.send(self._send_buffer[0])
                if len(self._send_buffer[0]) == writen:
                    del self._send_buffer[0]
                else:
                    self._send_buffer[0] = self._send_buffer[0][writen:]

    def send(self, data):
        self._send_buffer.append(self._encode_data(data) + self.EOL)

    def _encode_data(self, data):
        return base64.b64encode(data)

    def _decode_data(self, data):
        return base64.b64decode(data)
