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


class RegisterConcersContent(object):

    ALL_SWITCHES = 0

    def __init__(self, controller, concern_types):
        self.controller = controller
        # {type: [Switch] or ALL_SWITCHES for all switches}
        self.types = concern_types

    def serialize(self):
        types = {}
        for type, switches in self.types.items():
            if switches != self.ALL_SWITCHES:
                types[type] = []
                for switch in switches:
                    types[type].append(switch.serialize())
            else:
                types[type] = switches
        return (self.controller.serialize(), types)

    @classmethod
    def deserialize(cls, data):
        print data
        types = {}
        for type, switches in data[1].items():
            print switches
            if switches != cls.ALL_SWITCHES:
                types[type] = set()
                for switch in switches:
                    types[type].add(Switch.deserialize(switch))
            else:
                types[type] = switches
        return cls(Controller.deserialize(data[0]), types)

    def __repr__(self):
        return object_to_string(self,
                    controller = self.controller,
                    types = self.types)


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


class Packet(object):
    '''
    报文，该类中的常量表示报文的类型
    '''

    HELLO = 1
    CONTROL_FROM_SWITCH = 2
    CONTROL_FROM_API = 3
    REGISTER_CONCERN = 4
    LOCAL_CONCERN = 5
    ROUTING = 6

    DESERIALIZER = {
            HELLO: HelloPacketContent,
            REGISTER_CONCERN: RegisterConcersContent,
            ROUTING: RoutingPacketContent,
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
