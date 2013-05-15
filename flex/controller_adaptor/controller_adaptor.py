'''
Created on 2013-5-12

@author: kfirst
'''

from flex.base.module import Module
from flex.base.handler import PacketHandler, StorageHandler, EventHandler
from flex.core import core
from flex.model.packet import Packet, SwitchPacketContent
from flex.model.device import Device
from flex.controller_adaptor.selection_algorithms import SelectionAlgorithms
from flex.base import event

logger = core.get_logger()


class ControllerAdaptor(Module, PacketHandler, StorageHandler, EventHandler):

    LOCAL_CONCERN = 'local_concern'
    GLOBAL_CONCERN = 'global_concern'
    GLOBAL_CONCERN_CONTROLLERS = 'global_concern_controllers'

    def __init__(self, app_name, algorithms):
        self._myself = core.myself.get_self_controller()
        self._app_name = app_name
        self._global_controllers = {}
        self._local_controllers = {}
        self._algorithms = []
        self._packet = Packet(Packet.CONTROL_FROM_SWITCH, None)
        self._packet.src = core.myself.get_self_controller()
        for algorithm, parameters in algorithms.items():
            try:
                self._algorithms.append((getattr(SelectionAlgorithms, algorithm), parameters))
            except AttributeError:
                logger.warning('Algorithm ' + algorithm + ' is not found!')

    def start(self):
        self._app = getattr(core, self._app_name)
        core.forwarding.register_handler(Packet.CONTROL_FROM_API, self)
        core.event.register_handler(event.FlexUpEvent, self)
        core.globalStorage.listen_domain(self, self.GLOBAL_CONCERN, True)

    def handle_event(self, event):
        controllers = core.globalStorage.sget(self.GLOBAL_CONCERN_CONTROLLERS,
                            self.GLOBAL_CONCERN_CONTROLLERS)
        for controller in controllers:
            concerns = core.globalStorage.sget(controller, self.GLOBAL_CONCERN)
            controller = Device.deserialize(controller)
            for concern in concerns:
                concern = int(concern)
                try:
                    self._global_controllers[concern].add(controller)
                except KeyError:
                    self._global_controllers[concern] = set([controller])
                self._app.register(concern)

    def handle_packet(self, packet):
        self._app.process(packet.content)

    def handle_storage(self, key, value, domain, type):
        controller = Device.deserialize(key)
        if domain == self.GLOBAL_CONCERN:
            for concern_type in value:
                try:
                    self._global_controllers[concern_type].add(controller)
                except KeyError:
                    self._global_controllers[concern_type] = set([controller])
                self._app.register(concern_type)
        else:
            switch_id = domain[len(self.LOCAL_CONCERN) + 1:]
            switch = Device.deserialize(switch_id)
            for concern_type in value:
                try:
                    switches = self._local_controllers[concern_type]
                except KeyError:
                    switches = {}
                    self._local_controllers[concern_type] = switches
                try:
                    switches[switch].add(controller)
                except KeyError:
                    switches[switch] = set([controller])
                self._app.register(concern_type, switch)

    def forward(self, pox_content):
        self._handle_pox_content(pox_content)
        controllers = self._get_controllers(pox_content.type, pox_content.src)
        for algorithm, parameter in self._algorithms:
            controllers = algorithm(controllers, *parameter)
        self._send_packet(pox_content, controllers)

    def _handle_pox_content(self, pox_content):
        if pox_content.type != SwitchPacketContent.CONNECTION_UP:
            return
        switch_id = pox_content.src.get_id()
        core.globalStorage.listen_domain(self, '%s:%s' % (self.LOCAL_CONCERN, switch_id), True)
        core.routing.connected(pox_content.src, self._myself.get_address())

    def _send_packet(self, pox_content, controllers):
        self._packet.content = pox_content
        for controller in controllers:
            self._packet.dst = controller
            core.forwarding.forward(self._packet)

    def _get_controllers(self, type, switch):
        controllers = set()
        try:
            controllers.update(self._global_controllers[type])
        except KeyError:
            pass
        try:
            controllers.update(self._local_controllers[type][switch])
        except KeyError:
            pass
        return controllers
