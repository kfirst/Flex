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

    def __str__(self):
        return object_to_string(self, self.__id)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.__id)

    def __eq__(self, other):
        if isinstance(other, Device):
            return self.__id == other.__id
        return False


class Controller(Device):

    def __init__(self, cid, address):
        super(Controller, self).__init__(cid)
        self.__address = tuple(address)

    def get_address(self):
        return self.__address

    def __str__(self):
        return object_to_string(self, self.get_id(), self.__address)


class Switch(Device):

    def __init__(self, sid):
        super(Switch, self).__init__(sid)


if __name__ == '__main__':
    controller1 = Controller('cid', ('127.0.0.1', 1100))
    controller2 = Controller('cid', ('127.0.0.1', 1100))
    s = {}
    s[controller1] = 1
    s[controller2] = 2
    print s
