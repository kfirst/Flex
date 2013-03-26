# encoding: utf-8
'''
控制报文

@author: kfirst
'''

class PacketHeader(object):

    def __init__(self, src, dst, packet_type):
        self.src = src
        self.dst = dst
        self.type = packet_type
        self.path = []


class Packet(object):

    def __init__(self, header, content):
        self.header = header
        self.content = content


class TopologyPacketContent(object):

    def __init__(self, controller, switches_added, switches_removed):
        self.controller = controller
        self.switches_added = switches_added
        self.switches_removed = switches_removed
