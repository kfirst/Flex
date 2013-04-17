'''
Created on 2013-4-17

@author: kfirst
'''

from flex.core import core
from flex.base.handler import PacketHandler
from flex.model.packet import Packet
import time

core.set_config_path('../config')
core.start()
forwarding = core.forwarding

class Handler(PacketHandler):

    def handle(self, packet):
        print packet

packet = Packet('packet_type', 'content')

forwarding.forward(packet)
forwarding.register_handler('packet_type', Handler())
forwarding.forward(packet)

time.sleep(1)
