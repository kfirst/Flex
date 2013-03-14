# encoding: utf-8
'''
socket监听

@author: kfirst
'''

import select

class ConnectionMonitor(object):

    def __init__(self):
        self._connections = {}
        self._epoll = select.epoll()

    def add(self, connection):
        fd = connection.get_fileno()
        self._connections[fd] = connection
        self._epoll.register(fd, select.EPOLLIN | select.EPOLLOUT)

    def remove(self, connection):
        fd = connection.get_fileno()
        del self._connections[fd]
        self._epoll.unregister(fd)

    def schedule(self, timeout = 0):
        events = self._epoll.poll(timeout)
        for fd, event in events:
            self._connections[fd].handle(event)

    def __del__(self):
        for fd in self._connections:
            self.__epoll.unregister(fd)
        self._epoll.close()
