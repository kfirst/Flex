'''
Created on 2013-5-19

@author: kfirst
'''
import base64
import select
from flex.base.handler import ConnectionHandler
from flex.network.connection import Connection
import multiprocessing


class Receiver(object):

    def __init__(self, logger, address, backlog, buffer_size):
        self._logger = logger
        self._queue = multiprocessing.Queue(buffer_size)
        self._address = address
        self._backlog = backlog
        # fd => connection
        self._in_connections = {}
        # fd => connection_handler
        self._in_handlers = {}
        self._epoll = select.epoll()

        self._process = multiprocessing.Process(target = self._schedule)
        self._process.daemon = True
        self._process.start()

    def get_queue(self):
        return self._queue

    def _schedule(self):
        self._start_server()
        try:
            while 1:
                events = self._epoll.poll(-1)
                for fd, event in events:
                    try:
                        self._in_handlers[fd].handle(event)
                    except:
                        pass
        except:
            for fd, connection in self._in_connections.items():
                connection.close()
            self._epoll.close()

    def _start_server(self):
        server = Connection.get_server(self._address, self._backlog)
        fd = server.get_fileno()
        self._in_connections[fd] = server
        self._in_handlers[fd] = ServerHandler(server, self)
        self._epoll.register(fd, select.EPOLLIN)

    def _handle_data(self, data):
        self._queue.put(data)

    def _accept_in_connection(self, connection):
        connection = connection.accept(4096)
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


class ServerHandler(ConnectionHandler):

    def __init__(self, connection, network):
        self._connection = connection
        self._network = network

    def handle(self, event):
        self._network._accept_in_connection(self._connection)


class ClientHandler(ConnectionHandler):

    EOL = b'#'
    EOL_LENGTH = len(EOL)

    def __init__(self, connection, network):
        self._connection = connection
        self._network = network
        self._receive_buffer = b''

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
