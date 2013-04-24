'''
Created on 2013-4-24

@author: kfirst
'''

from flex.lib.util import object_to_string, parse_packet
from flex.model.packet import PacketOutContent, FlowModContent

class BaseMessage(object):

    def __init__(self):
        from flex.api.structures import Switch

    def __str__(self):
        return object_to_string(self)

    def __repr__(self):
        return self.__str__()


class ConnectionUpMessage(BaseMessage):

    def __init__(self, api, content):
        super(ConnectionUpMessage, self).__init__()
        self.switch = Switch(api, content.src)

    def __str__(self):
        return object_to_string(self,
                switch = self.switch)


class ConnectionDownMessage(BaseMessage):

    def __init__(self, api, content):
        super(ConnectionDownMessage, self).__init__()
        self.switch = Switch(api, content.src)

    def __str__(self):
        return object_to_string(self,
                switch = self.switch)


class PacketInMessage(BaseMessage):

    def __init__(self, api, content):
        super(PacketInMessage, self).__init__()
        self.switch = Switch(api, content.src)
        self.port = content.port
        self.data = content.data
        self._parsed = None

    @property
    def parsed(self):
        if self._parsed is None:
            self._parsed = parse_packet(self.data)
        return self._parsed


class PacketOutMessage(PacketOutContent):

    def __init__(self):
        super(PacketOutMessage, self).__init__(None)

    def to_content(self, switch):
        self.dst = switch
        return self


class FlowModMessage(FlowModContent):

    def __init__(self):
        super(FlowModMessage, self).__init__(None)

    def to_content(self, switch):
        self.dst = switch
        return self
