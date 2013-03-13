# encoding: utf-8
'''
socket监听

@author: kfirst
'''

import select

class SocketMonitor(object):

    def __init__(self, address, backlog):
        self.__listeners = {}
        self.__sockets = {}
        self.__requests = {}
        self.__epoll = select.epoll()

    def add_socket(self, sock, socket_listener):
        fd = sock.fileno()
        self.__listeners[fd] = socket_listener
        self.__sockets[fd] = sock
        self.__requests[fd] = b'';
        self.__epoll.register(fd, select.EPOLLIN)

    def schedule(self, timeout = 0):
        events = self.__epoll.poll(timeout)
        for fd, event in events:
            if event & select.EPOLLIN:
                listener = self.__listeners[fd]
                listener.handle(self.__sockets[fd])
            elif event & select.EPOLLHUP:
                self.__epoll.unregister(fd)

    def __del__(self):
        for fd in self.__sockets:
            self.__epoll.unregister(fd)
        self.__epoll.close()
