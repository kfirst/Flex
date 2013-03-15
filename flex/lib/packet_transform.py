# encoding: utf-8
'''
Created on 2013-3-15

@author: kfirst
'''

import pickle

class PacketTransform(object):

    def packet_to_data(self, packet):
        return pickle.dumps(packet, pickle.HIGHEST_PROTOCOL)

    def data_to_packet(self, data):
        return pickle.loads(data)


if __name__ == '__main__':
    from flex.model.packet import Packet
    from flex.model.packet import PacketHeader
    header = PacketHeader('src', 'dst', 'type')
    header.add_to_path('path')
    p = Packet(header, 'content')
    print p.__dict__
    j = PacketTransform().packet_to_data(p)
    print j
    p = PacketTransform().data_to_packet(j)
    print p.__dict__
    j = PacketTransform().packet_to_data(p)
    print j


