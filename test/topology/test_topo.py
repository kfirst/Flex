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

print topology._relation_of_neighbor
print topology._switches
'''
test_controller = topology._controllers['c_01_pox']
print topology.next_hop_of_controller(test_controller)
'''
self_controller = topology._controllers['c_01']

sw01 = Switch('sw01')
sw02 = Switch('sw02')
sw03 = Switch('sw03')
sw = set([sw01, sw02, sw03])

topo_packet_content = TopologyPacketContent(topology._controllers['c_01_pox'], sw, set())
topo_packet = Packet(PacketHeader.TOPO, topo_packet_content)
core.network.send(topology._controllers[topology._my_id], topo_packet)

time.sleep(1)

print topology._switches




