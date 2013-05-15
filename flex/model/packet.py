# encoding: utf-8
'''
报文

@author: kfirst
'''

from flex.lib.util import object_to_string
from flex.model.device import Controller, Switch, Device
from flex.model.action import Action
from flex.model.match import Match


class Packet(object):
    '''
    报文，该类中的常量表示报文的类型
    '''

    HELLO = 1
    CONTROL_FROM_SWITCH = 2
    CONTROL_FROM_API = 3
    ROUTING = 4
    STORAGE = 5

    DESERIALIZER = None

    def __init__(self, packet_type, content):
        self.src = None
        self.dst = None
        self.type = packet_type
        self.content = content

    def serialize(self):
        return (self.src.serialize(),
                self.dst.serialize(),
                self.type, self.content.serialize())

    @classmethod
    def deserialize(cls, data):
        deserializer = cls.DESERIALIZER[data[2]]
        content = deserializer.deserialize(data[3])
        packet = Packet(data[2], content)
        packet.src = Device.deserialize(data[0])
        packet.dst = Device.deserialize(data[1])
        return packet

    def __repr__(self):
        return object_to_string(self,
                    type = self.type,
                    content = self.content)


class HelloPacketContent(object):

    def __init__(self, controller, response = False):
        self.controller = controller
        self.response = response

    def serialize(self):
        return (self.controller.serialize(), self.response)

    @classmethod
    def deserialize(cls, data):
        return cls(Controller.deserialize(data[0]), data[1])

    def __repr__(self):
        return object_to_string(self,
                    controller = self.controller,
                    response = self.response)


class RoutingPacketContent(object):

    def __init__(self, controller, controllers_update, controllers_remove):
        self.controller = controller
        self.update = controllers_update
        self.remove = controllers_remove

    def serialize(self):
        update = []
        for controller, path in self.update:
            update.append((controller.serialize(), list(path)))
        remove = []
        for controller in self.remove:
            update.append(controller.serialize())
        return (self.controller.serialize(), update, remove)

    @classmethod
    def deserialize(cls, data):
        update = []
        for controller, path in data[1]:
            update.append((Device.deserialize(controller), set(path)))
        remove = []
        for controller in data[2]:
            update.append(Device.deserialize(controller))
        return cls(Device.deserialize(data[0]), update, remove)

    def __repr__(self):
        return object_to_string(self,
                    controller = self.controller,
                    update = self.update,
                    remove = self.remove)


class StoragePacketContent(object):

    def __init__(self, key, value, domain, type):
        self.key = key
        self.value = value
        self.domain = domain
        self.type = type

    def serialize(self):
        return (self.key, self.value, self.domain, self.type)

    @classmethod
    def deserialize(cls, data):
        return cls(*data)

    def __repr__(self):
        return object_to_string(self,
                    key = self.key,
                    value = self.value,
                    domain = self.domain,
                    type = self.type)




class SwitchPacketContent(object):

    PACKET_IN = 1
    CONNECTION_UP = 2
    CONNECTION_DOWN = 3

    DESERIALIZER = None

    def __init__(self, content_type, src):
        self.type = content_type
        self.src = src

    @classmethod
    def deserialize(cls, data):
        deserializer = cls.DESERIALIZER[data[0]]
        return deserializer.deserialize(data)


class ConnectionUpContent(SwitchPacketContent):

    def __init__(self, switch):
        super(ConnectionUpContent, self).__init__(
                SwitchPacketContent.CONNECTION_UP, switch)

    def serialize(self):
        return (self.type, self.src.serialize())

    @classmethod
    def deserialize(cls, data):
        return cls(Device.deserialize(data[1]))

    def __repr__(self):
        return object_to_string(self,
                    src = self.src)


class ConnectionDownContent(SwitchPacketContent):

    def __init__(self, switch):
        super(ConnectionUpContent, self).__init__(
                SwitchPacketContent.CONNECTION_DOWN, switch)

    def serialize(self):
        return (self.type, self.src.serialize())

    @classmethod
    def deserialize(cls, data):
        return cls(Device.deserialize(data[1]))

    def __repr__(self):
        return object_to_string(self,
                    src = self.src)


class PacketInContent(SwitchPacketContent):

    def __init__(self, switch):
        super(PacketInContent, self).__init__(
                SwitchPacketContent.PACKET_IN, switch)
        self.buffer_id = None
        self.port = None
        self.data = None

    def serialize(self):
        return (self.type, self.src.serialize(),
                self.buffer_id,
                self.port,
                self.data)

    @classmethod
    def deserialize(cls, data):
        content = cls(Device.deserialize(data[1]))
        content.buffer_id = data[2]
        content.port = data[3]
        content.data = data[4]
        return content

    def __repr__(self):
        return object_to_string(self,
                    src = self.src,
                    buffer_id = self.buffer_id,
                    port = self.port,
                    data_len = len(self.data))




class ApiPacketContent(object):

    PACKET_OUT = 1
    FLOW_MOD = 2

    DESERIALIZER = {}

    def __init__(self, content_type, dst):
        self.type = content_type
        self.dst = dst

    @classmethod
    def register_deserializer(cls, content_type):
        cls.DESERIALIZER[content_type] = cls

    @classmethod
    def deserialize(cls, data):
        deserializer = cls.DESERIALIZER[data[0]]
        return deserializer.deserialize(data)


class PacketOutContent(ApiPacketContent):

    def __init__(self, switch):
        super(PacketOutContent, self).__init__(
                ApiPacketContent.PACKET_OUT, switch)
        self.port = None
        self.buffer_id = None
        self.data = b''
        self.actions = []

    def serialize(self):
        actions = [action.serialize() for action in self.actions]
        return (self.type, self.dst.serialize(),
                self.port,
                self.buffer_id,
                self.data,
                actions)

    @classmethod
    def deserialize(cls, data):
        content = cls(Device.deserialize(data[1]))
        content.port = data[2]
        content.buffer_id = data[3]
        content.data = data[4]
        content.actions = [Action.deserialize(action) for action in data[5]]
        return content

    def __repr__(self):
        return object_to_string(self, self.dst,
                    port = self.port,
                    buffer_id = self.buffer_id,
                    data_len = len(self.data),
                    actions = self.actions)


class FlowModContent(ApiPacketContent):

    def __init__(self, switch):
        super(FlowModContent, self).__init__(
                ApiPacketContent.FLOW_MOD, switch)
        self.idle_timeout = 0
        self.hard_timeout = 0
        self.match = None
        self.buffer_id = None
        self.actions = []
        self.data = None

    def serialize(self):
        actions = [action.serialize() for action in self.actions]
        return (self.type, self.dst.serialize(),
                self.idle_timeout,
                self.hard_timeout,
                self.match.serialize(),
                self.buffer_id,
                actions,
                self.data)

    @classmethod
    def deserialize(cls, data):
        content = cls(Device.deserialize(data[1]))
        content.idle_timeout = data[2]
        content.hard_timeout = data[3]
        content.match = Match.deserialize(data[4])
        content.buffer_id = data[5]
        content.actions = [Action.deserialize(action) for action in data[6]]
        content.data = data[7]
        return content

    def __repr__(self):
        return object_to_string(self, self.dst,
                    port = self.port,
                    buffer_id = self.buffer_id,
                    data_len = len(self.data),
                    actions = self.actions)




Packet.DESERIALIZER = {
    Packet.HELLO: HelloPacketContent,
    Packet.ROUTING: RoutingPacketContent,
    Packet.STORAGE: StoragePacketContent,
    Packet.CONTROL_FROM_SWITCH: SwitchPacketContent,
    Packet.CONTROL_FROM_API: ApiPacketContent,
}

SwitchPacketContent.DESERIALIZER = {
    SwitchPacketContent.PACKET_IN: PacketInContent,
    SwitchPacketContent.CONNECTION_UP: ConnectionUpContent,
    SwitchPacketContent.CONNECTION_DOWN: ConnectionDownContent,
}

ApiPacketContent.DESERIALIZER = {
    ApiPacketContent.PACKET_OUT: PacketOutContent,
    ApiPacketContent.FLOW_MOD: FlowModContent,
}
