'''
Created on 2013-4-1

@author: fzm
'''
from flex.core import core
from flex.model.device import Device, Controller, Switch
from flex.model.packet import Packet, PacketHeader, HelloPacketContent, TopologyPacketContent
import time

core.set_config_path('../../config')
core.start()
topology = core.topology


'''
test_controller = topology._controllers['c_01_pox']
print topology.next_hop_of_controller(test_controller)
'''
self_controller = topology._controllers[topology._my_id]

sw01 = Switch('sw01')
sw02 = Switch('sw02')
sw03 = Switch('sw03')
sw04 = Switch('sw04')
sw05 = Switch('sw05')
sw06 = Switch('sw06')
sw07 = Switch('sw07')



sw = set([sw01, sw02, sw03])
topo_packet_content = TopologyPacketContent(topology._controllers['c_02_pox'], sw, set())
topo_packet = Packet(PacketHeader.TOPO, topo_packet_content)
core.network.send(topology._controllers[topology._my_id], topo_packet)

time.sleep(1)

sw = set([sw06, sw05, sw04])
topo_packet_content = TopologyPacketContent(topology._controllers['c_01'], sw, set())
topo_packet = Packet(PacketHeader.TOPO, topo_packet_content)
core.network.send(topology._controllers[topology._my_id], topo_packet)

time.sleep(1)

sw = set([sw07])
sw1 = set([sw01])
topo_packet_content = TopologyPacketContent(topology._controllers['c_02_pox'], sw, sw1)
topo_packet = Packet(PacketHeader.TOPO, topo_packet_content)
core.network.send(topology._controllers[topology._my_id], topo_packet)

time.sleep(1)

sw = set([sw07, sw06])
sw1 = set([sw01])
topo_packet_content = TopologyPacketContent(topology._controllers['c_02_pox'], sw, sw1)
topo_packet = Packet(PacketHeader.TOPO, topo_packet_content)
core.network.send(topology._controllers[topology._my_id], topo_packet)

time.sleep(1)

###################################################
hello_packet_content = HelloPacketContent(topology._controllers['c_02_pox'])
hello_packet = Packet(PacketHeader.HELLO, hello_packet_content)
core.network.send(topology._controllers[topology._my_id], hello_packet)
time.sleep(1)
hello_packet_content = HelloPacketContent(topology._controllers['c_01'])
hello_packet = Packet(PacketHeader.HELLO, hello_packet_content)
core.network.send(topology._controllers[topology._my_id], hello_packet)
time.sleep(1)



# print topology._switches
print topology._controllers_of_switch
print topology.next_hop_of_switch(sw02)





