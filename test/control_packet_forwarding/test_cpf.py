'''
Created on 2013-4-8

@author: fzm
'''
from flex.core import core
import time
from flex.model.packet import Packet, RegisterConcersContent, HelloPacketContent, TopologyPacketContent, ControlPacketContent
from flex.model.device import Device, Controller, Switch

core.set_config_path('../config')
core.start()
print 'sddsad'

##############################
hello_packet_content = HelloPacketContent(core.topology._controllers['c_02_pox'])
hello_packet = Packet(Packet.HELLO, hello_packet_content)
core.network.send(core.topology._controllers[core.topology._my_id], hello_packet)
time.sleep(1)

hello_packet_content = HelloPacketContent(core.topology._controllers['c_01_pox'])
hello_packet = Packet(Packet.HELLO, hello_packet_content)
core.network.send(core.topology._controllers[core.topology._my_id], hello_packet)
time.sleep(1)

hello_packet_content = HelloPacketContent(core.topology._controllers['c01'])
hello_packet = Packet(Packet.HELLO, hello_packet_content)
core.network.send(core.topology._controllers[core.topology._my_id], hello_packet)
time.sleep(1)

hello_packet_content = HelloPacketContent(core.topology._controllers['c02'])
hello_packet = Packet(Packet.HELLO, hello_packet_content)
core.network.send(core.topology._controllers[core.topology._my_id], hello_packet)
time.sleep(1)

hello_packet_content = HelloPacketContent(core.topology._controllers['c_01'])
hello_packet = Packet(Packet.HELLO, hello_packet_content)
core.network.send(core.topology._controllers[core.topology._my_id], hello_packet)
time.sleep(1)
##############################
cpf = core.controlpacketforwarding

self_id = cpf.self_id

controller = core.topology._controllers[self_id]

print 'I am ' + self_id

controller1 = core.topology._controllers['c01']
controller2 = core.topology._controllers['c02']
controller3 = core.topology._controllers['c_02_pox']
controller4 = core.topology._controllers['c_01']

content = RegisterConcersContent(controller1, set([1, 4, 6, 88]))
packet = Packet(Packet.REGISTEER_CONCERS, content)
core.network.send(controller, packet)

time.sleep(1)

content = RegisterConcersContent(controller2, set([1, 4, 7, 99]))
packet = Packet(Packet.REGISTEER_CONCERS, content)
core.network.send(controller, packet)

time.sleep(1)

content = RegisterConcersContent(controller2, set([11, 4, 47, 499]))
packet = Packet(Packet.REGISTEER_CONCERS, content)
core.network.send(controller, packet)

time.sleep(1)

content = RegisterConcersContent(controller4, set([1, 44, 47, 499]))
packet = Packet(Packet.REGISTEER_CONCERS, content)
core.network.send(controller, packet)

time.sleep(1)
###############################################
content = ControlPacketContent(11)
packet = Packet(Packet.CONTROL_FROM_SWITCH, content)
core.network.send(controller, packet)

time.sleep(1)


print cpf.type_controller

