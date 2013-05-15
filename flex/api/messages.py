'''
Created on 2013-4-24

@author: kfirst
'''

from flex.lib.util import object_to_string, parse_packet
from flex.model.packet import PacketOutContent, FlowModContent


class SwitchMessage(object):

    def __init__(self, content):
        from flex.api.structures import Switch
        self.switch = Switch.get_switch(content.src)

    def __repr__(self):
        return object_to_string(self,
                switch = self.switch)


class ConnectionUpMessage(SwitchMessage):

    def __init__(self, content):
        super(ConnectionUpMessage, self).__init__(content)


class ConnectionDownMessage(SwitchMessage):

    def __init__(self, content):
        super(ConnectionDownMessage, self).__init__(content)


class PacketInMessage(SwitchMessage):

    def __init__(self, content):
        super(PacketInMessage, self).__init__(content)
        self.buffer_id = content.buffer_id
        self.port = content.port
        self.data = content.data




class PacketOutMessage(object):

    content = PacketOutContent(None)

    def __init__(self):
        self.buffer_id = None
        self.port = None
        self.data = b''
        self.actions = []

    def to_content(self, switch):
        self.content.dst = switch
        self.content.buffer_id = self.buffer_id
        self.content.port = self.port
        self.content.data = self.data
        self.content.actions = self.actions
        return self


class FlowModMessage(object):

    def __init__(self):
        self.buffer_id = None
        self.port = None
        self.idle_timeout = 0
        self.hard_timeout = 0
        self.match = None
        self.actions = []

    def to_content(self, switch):
        self.dst = switch
        return self
