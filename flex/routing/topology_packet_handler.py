'''
Created on 2013-4-21

@author: kfirst
'''

from flex.core import core
import time

logger = core.get_logger()

class TopologyPacketHandler(object):

    def __init__(self, myself):
        self._myself = myself
        self._my_id = myself.get_id();
        # {controller: {controller: path}}
        self._nexthops_of_device = {}
        # {controller: (controller, path)}
        self._nexthop_of_device = {}
        self._connection_time = {}

    def _send_packet(self, packet, dst):
        packet.src = self._myself
        packet.dst = dst
        core.forwarding.forward(packet)

    def nexthop_of_device(self, device):
        return self._nexthop_of_device[device][0]

    def distance_of_device(self, device):
        return len(self._nexthop_of_device[device][1])

    def connecion_time_of_device(self, device):
        return self._connection_time[device]

    def _remove(self, src, removed_devices):
        remove = []
        update = []
        for removed_device in removed_devices:
            try:
                nexthop, path = self._nexthop_of_device[removed_device]
                nexthops = self._nexthops_of_device[removed_device]
                nexthops.pop(src, None)
                if src == nexthop:
                    shortest = None
                    for nexthop, path in nexthops.items():
                        if shortest == None or len(path) < len(shortest[1]):
                            shortest = [nexthop, path]
                    if shortest == None:
                        del self._nexthop_of_device[removed_device]
                        del self._connection_time[removed_device]
                        remove.append(removed_device)
                    else:
                        self._nexthop_of_device[removed_device] = shortest
                        update.append((removed_device, shortest[1]))
            except KeyError:
                logger.warning(str(removed_device) + ' is not found!');
        return (remove, update)

    def _update(self, src, updated_devices):
        update = []
        for updated_device, updated_path in updated_devices:
            if self._my_id in updated_path:
                continue
            updated_path.add(self._my_id)
            try:
                nexthop, path = self._nexthop_of_device[updated_device]
                nexthops = self._nexthops_of_device[updated_device]
                nexthops[src] = updated_path
                if nexthop == src:
                    if len(updated_path) <= len(path):
                        self._nexthop_of_device[updated_device] = [src, updated_path]
                        update.append((updated_device, updated_path))
                    else:
                        shortest = None
                        for nexthop, path in nexthops.items():
                            if shortest == None or len(path) < len(shortest[1]):
                                shortest = [nexthop, path]
                        self._nexthop_of_device[updated_device] = shortest
                        update.append((updated_device, shortest[1]))
                elif len(updated_path) < len(path):
                    self._nexthop_of_device[updated_device] = [src, updated_path]
                    update.append((updated_device, updated_path))
            except KeyError:
                self._nexthops_of_device[updated_device] = {src: updated_path}
                self._nexthop_of_device[updated_device] = [src, updated_path]
                self._connection_time[updated_device] = time.time()
                update.append((updated_device, updated_path))
        return update
