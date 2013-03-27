from flex.core import core
from flex.topology.topology import TopoHandler
from flex.topology.topology_parser import TopologyParser

def launch(path):
    topology_parser = TopologyParser(core.config)
    topo = TopoHandler()
    
    topo._controller_id = topology_parser.my_id
        
    topo._controller_controllers = topology_parser.controllers
    topo._controller_nexthop = topology_parser.nexthop
    topo._controller_neighbors = topology_parser.neighbors
    topo._controller_relations = topology_parser.relations
        
    core.register_object('topology', topo)
