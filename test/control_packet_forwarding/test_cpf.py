'''
Created on 2013-4-8

@author: fzm
'''
from flex.core import core
import time
from flex.model.packet import Packet, RegisterConcersContent, HelloPacketContent, TopologyPacketContent, ControlPacketContent, ApiPacketContent
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

sw01 = Switch('sw01')
sw02 = Switch('sw02')
sw03 = Switch('sw03')
sw04 = Switch('sw04')
sw05 = Switch('sw05')
sw06 = Switch('sw06')
sw07 = Switch('sw07')


###############################################################
sw = set([sw01, sw02, sw03])
topo_packet_content = TopologyPacketContent(core.topology._controllers['c_02_pox'], sw, set())
topo_packet = Packet(Packet.TOPO, topo_packet_content)
core.network.send(core.topology._controllers[core.topology._my_id], topo_packet)

time.sleep(1)

sw = set([sw06, sw05, sw04])
topo_packet_content = TopologyPacketContent(core.topology._controllers['c_01_pox'], sw, set())
topo_packet = Packet(Packet.TOPO, topo_packet_content)
core.network.send(core.topology._controllers[core.topology._my_id], topo_packet)

time.sleep(1)

content = ApiPacketContent(111, sw01)
packet = Packet(Packet.CONTROL_FROM_API, content)
core.network.send(controller, packet)

time.sleep(1)

print cpf.type
print core.topology._controllers_of_switch

