# encoding: utf-8
'''
各种处理程序
Created on 2013-3-14

@author: kfirst
'''

class ConnectionHandler(object):

    def set_connection(self, connection):
        self._connection = connection

    def handle(self, event):
        pass

    def send(self, data):
        pass


class DataHandler(object):
    '''
    处理网络传输信息的Handler，功能一般是将网络传输的信息转换为Packet结构
    '''
    def handle(self, data):
        pass


class PacketHandler(object):
    '''
    处理Packet的Handler，可以注册在Network模块中用于处理接收到的Packet
    '''
    def handle_packet(self, packet):
        pass


class EventHandler(object):
    '''
    处理事件的Handler，可以注册在Event模块处理相应的事件
    '''
    def handle_event(self, event):
        pass


class StorageHandler(object):

    def handle_storage(self, key, value, domain, type):
        pass
