# encoding: utf-8
'''
报文

@author: kfirst
'''

from flex.lib.util import object_to_string

class PacketHeader(object):

    TOPO = 1000
    HELLO = 2000

    def __init__(self, src, dst, packet_type):
        self.src = src
        self.dst = dst
        self.type = packet_type
        self.path = []

    def __str__(self, *args, **kwargs):
        return object_to_string(self,
                    type = self.type,
                    src = self.src,
                    dst = self.dst,
                    path = self.path)

class Packet(object):

    def __init__(self, header, content):
        self.header = header
        self.content = content

    def __str__(self, *args, **kwargs):
        return object_to_string(self,
                    header = self.header,
                    content = self.content)


class TopologyPacketContent(object):

    def __init__(self, controller, switches_added, switches_removed):
        self.controller = controller
        self.switches_added = switches_added
        self.switches_removed = switches_removed


if __name__ == '__main__':
    from flex.model.device import Controller
    controller = Controller('cid', ('ip', 'port'))
    header = PacketHeader(controller, controller, 'packet_type')
    packet = Packet(header, 'content')
    print packet
