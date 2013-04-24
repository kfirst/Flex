# encoding: utf-8
'''
报文

@author: kfirst
'''

from flex.lib.util import object_to_string
import time

class PacketTracker(object):
    '''
    报文追踪器，记录报文经过的路径，主要用于Debug
    '''

    def __init__(self):
        self._src = None
        self._dst = None
        self._path = []

    def track(self, src, dst):
        self._src = src.get_id()
        self._dst = dst.get_id()
        self._time = time.time()
        if not self._path:
            self._path.append(self._src)
        elif self._path[-1] != self._src:
            self._path.append(self._src)
            if len(self._path) > 5:
                self._path.pop(0)

    @property
    def src(self):
        return self._src

    def __repr__(self):
        return object_to_string(self,
                    src = self._src,
                    dst = self._dst,
                    path = self._path,
                    time = self._time)


class Packet(object):
    '''
    报文，该类中的常量表示报文的类型
    '''

    TOPO_SWITCH = 'topo_switch'
    TOPO_CONTROLLER = 'topo_controller'
    HELLO = 'hello'
    CONTROL_FROM_SWITCH = 'control_from_switch'
    LOCAL_TO_API = 'local_to_api'
    CONTROL_FROM_API = 'control_from_api'
    LOCAL_TO_POX = 'local_to_pox'
    REGISTER_CONCERN = 'register_concern'
    LOCAL_CONCERN = 'local_concern'

    def __init__(self, packet_type, content):
        self.tracker = PacketTracker()
        self.type = packet_type
        self.content = content

    def __repr__(self):
        return object_to_string(self,
                    type = self.type,
                    content = self.content,
                    tracker = self.tracker)


class TopologySwitchPacketContent(object):

    def __init__(self, controller, switches_update, switches_remove):
        self.controller = controller
        self.update = switches_update
        self.remove = switches_remove

    def __repr__(self):
        return object_to_string(self,
                    controller = self.controller,
                    update = self.update,
                    remove = self.remove)


class TopologyControllerPacketContent(object):

    def __init__(self, controller, controllers_update, controllers_remove):
        self.controller = controller
        self.update = controllers_update
        self.remove = controllers_remove

    def __repr__(self):
        return object_to_string(self,
                    controller = self.controller,
                    update = self.update,
                    remove = self.remove)


class HelloPacketContent(object):

    def __init__(self, controller, response = False):
        self.response = response
        self.controller = controller

    def __repr__(self):
        return object_to_string(self,
                    response = self.response,
                    controller = self.controller)


class RegisterConcersContent(object):

    ALL_SWITCHES = 0

    def __init__(self, controller, concern_types):
        self.controller = controller
        # {type: [Switch] or ALL_SWITCHES for all switches}
        self.types = concern_types

    def __repr__(self):
        return object_to_string(self,
                    controller = self.controller,
                    types = self.types)


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
