'''
Created on 2013-5-15

@author: kfirst
'''
from flex.base.module import Module
from flex.model.packet import *


class MessageApi(Module):

    def flow_mod_message(self):
        return FlowModContent(None)

    def packet_out_message(self):
        return PacketOutContent(None)
