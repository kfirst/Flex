# encoding: utf-8
'''
控制报文

@author: kfirst
'''

class PacketHeader(object):

    def __init__(self, src, dst, packet_type):
        self.__src = src
        self.__dst = dst
        self.__type = packet_type
        self.__path = []

    def add_to_path(self, device):
        self.__path.append(device)

    def get_src(self):
        return self.__src

    def get_dst(self):
        return self.__dst

    def get_type(self):
        return self.__type


class Packet(object):

    def __init__(self, header, content):
        self.__header = header
        self.__content = content

    def get_content(self):
        return self.__content
