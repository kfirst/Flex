from flex.core import core
from flex.topology.topology import Topology
from flex.topology.topology_parser import TopologyParser

def launch():
    topology_parser = TopologyParser(core.config)
    topo = Topology()

    topo._myself = topology_parser.myself
    topo._relation_of_neighbor = topology_parser.neighbors
    topo._neighbors_with_relation = topology_parser.relations

    core.register_object('topology', topo)
