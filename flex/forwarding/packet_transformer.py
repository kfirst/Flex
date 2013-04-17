# encoding: utf-8
'''
Created on 2013-3-15

@author: kfirst
'''

import pickle

class PacketTransformer(object):

    def packet_to_data(self, packet):
        return pickle.dumps(packet, pickle.HIGHEST_PROTOCOL)

    def data_to_packet(self, data):
        return pickle.loads(data)
