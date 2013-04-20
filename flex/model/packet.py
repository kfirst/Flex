# encoding: utf-8
'''
报文

@author: kfirst
'''

from flex.lib.util import object_to_string

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
        if not self._path:
            self._path.append(self._src)
        elif self._path[-1] != self._src:
            self._path.append(self._src)
            if len(self._path) > 5:
                self._path.pop(0)

    @property
    def src(self):
        return self._src

    def __str__(self):
        return object_to_string(self,
                    src = self._src,
                    dst = self._dst,
                    path = self._path)

    def __repr__(self):
        return self.__str__()


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

    def __str__(self):
        return object_to_string(self,
                    type = self.type,
                    content = self.content,
                    tracker = self.tracker)

    def __repr__(self):
        return self.__str__()


class TopologySwitchPacketContent(object):

    def __init__(self, controller, switches_update, switches_remove):
        self.controller = controller
        self.update = switches_update
        self.remove = switches_remove

    def __str__(self):
        return object_to_string(self,
                    controller = self.controller,
                    update = self.update,
                    remove = self.remove)

    def __repr__(self):
        return self.__str__()


class HelloPacketContent(object):

    def __init__(self, controller, response = False):
        self.response = response
        self.controller = controller

    def __str__(self):
        return object_to_string(self,
                    response = self.response,
                    controller = self.controller)

    def __repr__(self):
        return self.__str__()


class RegisterConcersContent(object):

    ALL_SWITCHES = 0

    def __init__(self, controller, concern_types):
        self.controller = controller
        # type => [switches] or [] for all switches
        self.types = concern_types

    def __str__(self):
        return object_to_string(self,
                    controller = self.controller,
                    types = self.types)


class ControlPacketContent(object):

    PACKET_IN = 'PacketIn'

    def __init__(self, content_type, switch):
        self.type = content_type
        self.switch = switch

    def __repr__(self):
        return self.__str__()


class PoxPacketContent(ControlPacketContent):

    def __init__(self, content_type, src):
        super(PoxPacketContent, self).__init__(content_type, src)

    def __str__(self):
        return object_to_string(self,
                    type = self.type,
                    src = self.switch)


class PacketInContent(PoxPacketContent):

    def __init__(self, switch, port, data):
        super(PacketInContent, self).__init__(
                ControlPacketContent.PACKET_IN, switch)
        self.port = port
        self.data = data


class ApiPacketContent(ControlPacketContent):

    def __init__(self, content_type, dst):
        super(ApiPacketContent, self).__init__(content_type, dst)

    def __str__(self):
        return object_to_string(self,
                    type = self.type,
                    dst = self.switch)
