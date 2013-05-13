# encoding: utf-8
'''
报文

@author: kfirst
'''

from flex.lib.util import object_to_string
from flex.model.device import Controller, Switch, Device


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

    def __init__(self, key, value, type):
        self.key = key
        self.value = value
        self.type = type

    def serialize(self):
        return (self.key, self.type)

    @classmethod
    def deserialize(cls, data):
        return cls(*data)

    def __repr__(self):
        return object_to_string(self,
                    key = self.key,
                    value = self.value,
                    type = self.type)


class Packet(object):
    '''
    报文，该类中的常量表示报文的类型
    '''

    HELLO = 1
    CONTROL_FROM_SWITCH = 2
    CONTROL_FROM_API = 3
    ROUTING = 4
    STORAGE = 5

    DESERIALIZER = {
            HELLO: HelloPacketContent,
            ROUTING: RoutingPacketContent,
            STORAGE: StoragePacketContent,
    }

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


class ControlPacketContent(object):

    PACKET_IN = 'PacketIn'
    CONNECTION_UP = 'ConnectionUp'
    CONNECTION_DOWN = 'ConnectionDown'
    PACKET_OUT = 'PacketOut'
    FLOW_MOD = 'FlowMod'

    def __init__(self, content_type, src, dst):
        self.type = content_type
        self.src = src
        self.dst = dst


class PoxPacketContent(ControlPacketContent):

    def __init__(self, content_type, src):
        super(PoxPacketContent, self).__init__(content_type, src, None)

    def __repr__(self):
        return object_to_string(self,
                    type = self.type,
                    src = self.src,
                    dst = self.dst)


class ConnectionUpContent(PoxPacketContent):

    def __init__(self, switch):
        super(ConnectionUpContent, self).__init__(
                ControlPacketContent.CONNECTION_UP, switch)


class ConnectionDownContent(PoxPacketContent):

    def __init__(self, switch):
        super(ConnectionUpContent, self).__init__(
                ControlPacketContent.CONNECTION_DOWN, switch)


class PacketInContent(PoxPacketContent):

    def __init__(self, switch, ofp):
        super(PacketInContent, self).__init__(
                ControlPacketContent.PACKET_IN, switch)
        self.ofp = ofp

    @property
    def port(self):
        return self.ofp.in_port

    @property
    def data(self):
        return self.ofp.data

    @property
    def buffer_id(self):
        return self.ofp.buffer_id


class ApiPacketContent(ControlPacketContent):

    def __init__(self, content_type, dst):
        super(ApiPacketContent, self).__init__(content_type, None, dst)

    def __repr__(self):
        return object_to_string(self,
                    type = self.type,
                    src = self.src,
                    dst = self.dst)


class PacketOutContent(ApiPacketContent):

    def __init__(self, switch):
        super(PacketOutContent, self).__init__(
                ControlPacketContent.PACKET_OUT, switch)
        self.port = None
        self.buffer_id = None
        self.data = b''
        self.actions = []


class FlowModContent(ApiPacketContent):

    def __init__(self, switch):
        super(FlowModContent, self).__init__(
                ControlPacketContent.FLOW_MOD, switch)
        self.idle_timeout = 0
        self.hard_timeout = 0
        self.match = None
        self.buffer_id = None
        self.actions = []
        self.data = None
