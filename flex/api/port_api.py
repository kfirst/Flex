'''
Created on 2013-5-15

@author: kfirst
'''
from flex.model.device import Port
from flex.base.module import Module


class PortApi(Module):

    def flood_port(self):
        return Port.FLOOD;
