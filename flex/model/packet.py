# encoding: utf-8
'''
控制报文

@author: kfirst
'''

class PacketHeader(object):

    def __init__(self, src, dst, type):
        self.src = src
        self.dst = dst
        self.type = type
        self.path = []


class Packet(object):

    def __init__(self, header, content):
        self.header = header
        self.content = content

class PacketContent(object):

    def __init__(self, ttype, controller, content):
        self.type = ttype
        self.controller = controller
        self.content = content

