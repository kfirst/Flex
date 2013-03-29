# encoding: utf-8
'''
Switch与Controller等网络设备

@author: kfirst
'''
from flex.lib.util import object_to_string

class Device(object):

    def __init__(self, device_id):
        self.__id = device_id

    def get_id(self):
        return self.__id

    def __str__(self, *args, **kwargs):
        return object_to_string(self, self.__id)


class Controller(Device):

    def __init__(self, cid, address):
        super(Controller, self).__init__(cid)
        self.__address = address
        self.__status = False

    def get_address(self):
        return self.__address

    def is_up(self):
        return self.__status

    def up(self):
        self.__status = True

    def down(self):
        self.__status = False


class Switch(Device):

    def __init__(self, sid):
        super(Switch, self).__init__(sid)


if __name__ == '__main__':
    controller = Controller('cid', 'address')
    print controller
