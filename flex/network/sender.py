'''
Created on 2013-5-19

@author: kfirst
'''

import multiprocessing
import base64
from flex.network.connection import Connection
from flex.base.exception import ConnectFailException
import time


class Sender(object):

    EOL = b'#'

    def __init__(self, logger, buffer_size):
        self._logger = logger
        self._queue = multiprocessing.Queue(buffer_size)
        self._out_connections = {}

        self._process = multiprocessing.Process(target = self._schedule)
        self._process.daemon = True
        self._process.start()

    def send(self, address, data):
        self._queue.put((address, data))

    def terminate(self):
        if self._process.is_alive():
            self._process.terminate()

    def _schedule(self):
        try:
            while 1:
                address, data = self._queue.get()
                to_send = '%s%s' % (base64.b64encode(data), self.EOL)
                while 1:
                    connection = self._get_out_connection(address)
                    if not connection:
                        break
                    try:
                        writen = connection.send(to_send)
                        break
                    except Exception:
                        self._remove_out_connection(address)
        except:
            for fd, connection in self._out_connections.items():
                connection.close()

    def _get_out_connection(self, address):
        try:
            connection = self._out_connections[address]
        except KeyError:
            try:
                connection = Connection.get_client(address, 1024 * 8)
                self._out_connections[address] = connection
            except ConnectFailException, e:
                self._logger.warning(e.message)
                return False
        return connection

    def _remove_out_connection(self, address):
        connection = self._out_connections.pop(address)
        connection.close()
