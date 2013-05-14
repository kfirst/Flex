# Copyright 2011 James McCauley
#
# This file is part of POX.
#
# POX is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# POX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with POX.  If not, see <http://www.gnu.org/licenses/>.

from flex.core import core
from flex.lib.util import str_to_bool
from flex.api import messages, structures
from flex.base.module import Module
import time

"""
An L2 learning switch.

It is derived from one written live for an SDN crash course.
It is somwhat similar to NOX's pyswitch in that it installs
exact-match rules for each flow.
"""

logger = core.get_logger()

# We don't want to flood immediately when a switch connects.
# Can be overriden on commandline.
_flood_delay = 0

class LearningSwitch (object):
    """
    The learning switch "brain" associated with a single OpenFlow switch.
    
    When we see a packet, we'd like to output it on a port which will
    eventually lead to the destination.  To accomplish this, we build a
    table that maps addresses to ports.
    
    We populate the table by observing traffic.  When we see a packet
    from some source coming from some port, we know that source is out
    that port.
    
    When we want to forward traffic, we look up the desintation in our
    table.  If we don't know the port, we simply send the message out
    all ports except the one it came in on.  (In the presence of loops,
    this is bad!).
    
    In short, our algorithm looks like this:
    
    For each packet from the switch:
    1) Use source address and switch port to update address/port table
    2) Is transparent = False and either Ethertype is LLDP or the packet's
       destination address is a Bridge Filtered address?
       Yes:
          2a) Drop packet -- don't forward link-local traffic (LLDP, 802.1x)
              DONE
    3) Is destination multicast?
       Yes:
          3a) Flood the packet
              DONE
    4) Port for destination address in our address/port table?
       No:
          4a) Flood the packet
              DONE
    5) Is output port the same as input port?
       Yes:
          5a) Drop packet and similar ones for a while
    6) Install flow table entry in the switch so that this
       flow goes out the appopriate port
       6a) Send the packet out appropriate port
    """

    def __init__ (self, connection, transparent):
        # Switch we'll be adding L2 learning switch capabilities to
        self.connection = connection
        self.transparent = transparent

        # Our table
        self.macToPort = {}

        # We want to hear PacketIn messages, so we listen
        # to the connection
        connection.add_listeners(self)

        # We just use this to know when to log a helpful message
        self.hold_down_expired = _flood_delay == 0

        # log.debug("Initializing LearningSwitch, transparent=%s",
        #          str(self.transparent))

    def _handle_PacketIn(self, event):
        """
        Handle packet in messages from the switch to implement above algorithm.
        """
        packet = event.parsed

        def flood (message = None):
            """ Floods the packet """
            msg = messages.PacketOutMessage()
            if time.time() - self.connection.connect_time >= _flood_delay:
                # Only flood if we've been connected for a little while...
                if self.hold_down_expired is False:
                    # Oh yes it is!
                    self.hold_down_expired = True
                    # logger.info("%s: Flood hold-down expired -- flooding", str(event.switch))

                if message is not None: logger.debug(message)
                # log.debug("%i: flood %s -> %s", event.dpid,packet.src,packet.dst)
                # OFPP_FLOOD is optional; on some switches you may need to change
                # this to OFPP_ALL.
                msg.actions.append(structures.OutputAction(port = structures.Port.flood()))
            else:
                pass
            logger.info("Holding down flood for %s", str(event.switch))
            msg.data = event.ofp
            msg.port = event.port
            self.connection.send(msg)

        def drop (duration = None):
            """
            Drops this packet and optionally installs a flow to continue
            dropping similar ones for a while
            """
            if duration is not None:
                if not isinstance(duration, tuple):
                    duration = (duration, duration)
                msg = messages.FlowModMessage()
                msg.match = structures.Match.from_packet(packet)
                msg.idle_timeout = duration[0]
                msg.hard_timeout = duration[1]
                msg.buffer_id = event.buffer_id
                self.connection.send(msg)
            elif event.ofp.buffer_id is not None:
                msg = messages.PacketOutMessage()
                msg.buffer_id = event.buffer_id
                msg.port = event.port
                self.connection.send(msg)

        self.macToPort[packet.src] = event.port  # 1

        if not self.transparent:  # 2
            if packet.type == packet.LLDP_TYPE or packet.dst.isBridgeFiltered():
                drop()  # 2a
                return

        if packet.dst.is_multicast:
            flood()  # 3a
        else:
            if packet.dst not in self.macToPort:  # 4
                flood("Port for %s unknown -- flooding" % (packet.dst,))  # 4a
            else:
                port = self.macToPort[packet.dst]
                if port == event.port:  # 5
                    # 5a
                    logger.warning("Same port for packet from %s -> %s on %s.%s.  Drop."
                                % (packet.src, packet.dst, event.switch, port))
                    drop(10)
                    return
                # 6
                logger.debug("installing flow for %s.%i -> %s.%i" %
                          (packet.src, event.port, packet.dst, port))
                msg = messages.FlowModMessage()
                msg.match = structures.Match.from_packet(packet, event.port)
                msg.idle_timeout = 10
                msg.hard_timeout = 30
                msg.actions.append(structures.OutputAction(port = port))
                msg.data = event.ofp  # 6a
                self.connection.send(msg)


class l2_learning (Module):
    """
    Waits for OpenFlow switches to connect and makes them learning switches.
    """
    def __init__ (self, transparent):
        self.transparent = transparent

    def start(self):
        core.api.all_switches.add_listeners(self)

    def _handle_ConnectionUp(self, event):
        logger.debug("Connection %s" % event.src)
        LearningSwitch(event.src, self.transparent)


def launch():
    """
    Starts an L2 learning switch.
    """
    transparent = core.config.get('module.l2_learning.transparent', False)
    hold_down = core.config.get('module.l2_learning.hold_down', _flood_delay)

    try:
        global _flood_delay
        _flood_delay = int(str(hold_down), 10)
        assert _flood_delay >= 0
    except:
        raise RuntimeError("Expected hold-down to be a number")
    core.register_component(l2_learning, str_to_bool(transparent))
