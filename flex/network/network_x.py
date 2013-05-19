'''
Created on 2013-5-19

@author: kfirst
'''

from flex.base.module import Module
from flex.base.handler import DataHandler
from flex.network.sender import Sender
from flex.network.receiver import Receiver
import threading
from flex.core import core

logger = core.get_logger()


class Network(Module):

    def __init__(self, address, backlog, buffer_size):
        self._data_handler = EmptyDataHandler()
        self._sender = Sender(logger, buffer_size)
        self._receiver = Receiver(logger, address, backlog, buffer_size)
        self._receive_queue = self._receiver.get_queue()

    def register_data_handler(self, data_handler):
        self._data_handler = data_handler

    def send(self, address, data):
        self._sender.send(address, data)

    def start(self):
        thread = threading.Thread(target = self._schedule)
        thread.setDaemon(True)
        thread.start()

    def _schedule(self):
        while 1:
            data = self._receive_queue.get()
            self._data_handler.handle(data)


class EmptyDataHandler(DataHandler):

    def handle(self, data):
        pass
