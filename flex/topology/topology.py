'''
Created on 2013-3-19

@author: fzm
'''

from flex.topology.find_hop_of_switch import FindHopOfSwitch
from flex.topology.find_hop_of_controller import FindHopOfController
from flex.model.device import Controller

class TopoHandler(object):

    def __init__(self, controller_id):
        self.id = controller_id
        self.topo_of_controller = {}
        self.provider_controller = set()
        self.peer_controller = set()
        self.customer_controller = set()
        self.controller_to_address = {}
        #self.switch = set()
        
        
        
        self.from_controller = FindHopOfController()
        self.from_switch = FindHopOfSwitch()

    def handle(self, packet):
        '''
        0:lower->upper
        1:peer
        2:pox
        '''
        if packet.content.type == 0:
            self.from_switch.modify_from_peer_controller(packet.content)
        elif packet.content.type == 1:
            self.from_switch.modify_from_customer_controller(packet.content)
        elif packet.content.type == 2:
            self.from_switch.modify_from_pox(packet.content)
            
    def next_hop_of_controller(self, controller):
        ans = self.from_controller.find_hop(self.id, controller.__id, self.topo_of_controller)
        if(ans == None):
            return None
        else:
            con = Controller(ans, self.id, self.controller_to_address[ans])
            return con
    def next_hop_of_switch(self, switch):
        return  self.from_switch.find_hop(switch.__id, self.topo_of_controller)
    