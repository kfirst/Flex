# encoding: utf-8
'''
报文

@author: kfirst
'''

from flex.lib.util import object_to_string

class PacketHeader(object):

    TOPO = 'topo'
    HELLO = 'hello'

    def __init__(self, src, dst, packet_type):
        self.src = src
        self.dst = dst
        self.type = packet_type
        self.path = []

    def __str__(self):
        return object_to_string(self,
                    type = self.type,
                    src = self.src,
                    dst = self.dst,
                    path = self.path)

    def __repr__(self):
        return self.__str__()


class Packet(object):

    def __init__(self, packet_type, content):
        self.header = PacketHeader(None, None, packet_type)
        self.content = content

    def __str__(self):
        return object_to_string(self,
                    header = self.header,
                    content = self.content)

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
                                switches_removed = self.switches_removed
                                )

    def __repr__(self):
        return self.__str__()


class HelloPacketContent(object):

    def __init__(self, controller):
        self.if_response = False
        self.controller = controller

    def __str__(self):
        return object_to_string(self,
                                if_response = self.if_response,
                                controller = self.controller
                                )

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    from flex.model.device import Controller
    controller = Controller('cid', ('ip', 'port'))
    packet = Packet('packet_header', 'content')
    print packet
