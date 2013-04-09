# encoding: utf-8
'''
报文

@author: kfirst
'''

from flex.lib.util import object_to_string

class PacketTracker(object):
    '''
    报文追踪器，记录报文经过的路径，主要用于Debug
    '''

    def __init__(self):
        self.src = None
        self.dst = None
        self.path = []

    def __str__(self):
        return object_to_string(self,
                    src = self.src,
                    dst = self.dst,
                    path = self.path)

    def __repr__(self):
        return self.__str__()


class Packet(object):
    '''
    报文，该类中的常量表示报文的类型
    '''

    TOPO = 'topo'
    HELLO = 'hello'
    CONTROL_FROM_SWITCH = 'control_from_switch'
    LOCAL_TO_API = 'local_to_api'
    CONTROL_FROM_API = 'control_from_api'
    LOCAL_TO_POX = 'local_to_pox'
    REGISTER_CONCERN = 'register_concern'
    LOCAL_CONCERN = 'local_concern'

    def __init__(self, packet_type, content):
        self.tracker = PacketTracker()
        self.type = packet_type
        self.content = content

    def __str__(self):
        return object_to_string(self,
                    type = self.type,
                    content = self.content,
                    tracker = self.tracker)

    def __repr__(self):
        return self.__str__()


class TopologyPacketContent(object):

    def __init__(self, controller, switches_added, switches_removed):
        self.controller = controller
        self.switches_added = switches_added
        self.switches_removed = switches_removed

    def __str__(self):
        return object_to_string(self,
                    controller = self.controller,
                    switches_added = self.switches_added,
                    switches_removed = self.switches_removed)

    def __repr__(self):
        return self.__str__()


class HelloPacketContent(object):

    def __init__(self, controller, response = False):
        self.response = response
        self.controller = controller

    def __str__(self):
        return object_to_string(self,
                    if_response = self.response,
                    controller = self.controller)

    def __repr__(self):
        return self.__str__()


class ControlPacketContent():

    CONNECTION_UP = 'ConnectionUp'
    CONNECTION_DOWN = 'ConnectionDown'

    def __init__(self, content_type):
        self.type = content_type

    def __str__(self):
        return object_to_string(self,
                    type = self.type)


class ConnectionUpContent(ControlPacketContent):

    def __init__(self, switch):
        super(ConnectionUpContent, self).__init__(ControlPacketContent.CONNECTION_UP)
        self.switch = switch


class ConnectionDownContent(ControlPacketContent):

    def __init__(self, switch):
        super(ConnectionDownContent, self).__init__(ControlPacketContent.CONNECTION_DOWN)
        self.switch = switch

class RegisterConcersContent(object):
    def __init__(self, controller, concern_type):
        self.controller = controller
        self.type = concern_type

    def __str__(self):
        return object_to_string(self,
                    controller = self.controller,
                    type = self.type)
