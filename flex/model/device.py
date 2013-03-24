# encoding: utf-8
'''
Switch与Controller等网络设备

@author: kfirst
'''

class Device(object):

    def __init__(self, device_id):
        self.__id = device_id

    def get_id(self):
        return self.__id


class Controller(Device):

    def __init__(self, cid, address, backlog):
        super(Controller, self).__init__(cid)
        self.__address = address
        self.__backlog = backlog

    def get_address(self):
        return self.__address

    def get_backlog(self):
        return self.__backlog


class Switch(Device):

    def __init__(self, sid):
        super(Switch, self).__init__(sid)
