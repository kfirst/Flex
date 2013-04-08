'''
Created on 2013-4-8

@author: fzm
'''
from flex.core import core
import time
from flex.model.packet import Packet, RegisterConcersContent

core.set_config_path('../config')
core.start()
print 'sddsad'
cpf = core.controlPacketForwarding

self_id = cpf.self_id

controller = core.topology._controllers[self_id]

print 'I am ' + self_id

controller1 = core.topology._controllers['c01']
controller2 = core.topology._controllers['c02']
controller3 = core.topology._controllers['c_02_pox']

'''
content = RegisterConcersContent(controller1, set[1, 4, 6, 88])
packet = Packet(Packet.REGISTEER_CONCERS, content)
core.network.send(controller, packet)
'''
time.sleep(1)

