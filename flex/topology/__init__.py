from flex.core import core
from flex.topology.topology import TopoHandler
from flex.topology.topology_parser import TopologyParser

def launch(path):
    topology_parser = TopologyParser(core.config)
    topo = TopoHandler()
    # TODO
    core.register_object('topology', topo)
