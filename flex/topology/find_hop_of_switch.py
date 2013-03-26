'''
Created on 2013-3-19

@author: fzm
'''
class FindHopOfSwitch(object):
    
    def __init__(self):
        self.switch = set()
    def find_hop(self, switch, topo_of_controller):
        pass
    def modify_from_peer_controller(self, content):
        self.switch = self.switch | content[0]
        self.switch = self.switch - content[1]
    def modify_from_customer_controller(self, content):
        self.switch = self.switch | content[0]
        self.switch = self.switch - content[1]
    def modify_from_pox(self, content):
        self.switch = self.switch | content[0]
        self.switch = self.switch - content[1]