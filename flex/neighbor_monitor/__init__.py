from flex.core import core
from flex.neighbor_monitor.neighbor_parser import NeighborParser
from flex.neighbor_monitor.neighbor_monitor import NeighborMonitor

def launch():
    neighbor_parser = NeighborParser(core.config)
    monitor = NeighborMonitor()

    monitor._myself = neighbor_parser.myself
    monitor._relation_of_neighbor = neighbor_parser.neighbors
    monitor._neighbors_with_relation = neighbor_parser.relations

    core.register_object('NeighborMonitor', monitor)
