from flex.core import core
from flex.topology.topology import TopoHandler

def launch(path):
    topo = TopoHandler()
    config = core.config
    #controller_id = config.get('module.topology.id')
    topo.id = config.get('module.topology.id')
    controller_topology = config.get('topology.controllers')
    for i in controller_topology:
        #单个controller信息
        if  i == topo.id:
            neighbor_controller = controller_topology[i]['neighbors']
            for j in neighbor_controller:
                if neighbor_controller[j] == 'provider':
                    topo.provider_controller.add(j)
                elif neighbor_controller[j] == 'peer':
                    topo.peer_controller.add(j)
                elif neighbor_controller[j] == 'customer':
                    topo.customer_controller.add(j)
        #整个topo信息
        neighbor_controller = controller_topology[i]['neighbors']
        set_controller = set()
        for j in neighbor_controller:
            set_controller.add(j)
        topo.topo_of_controller[i] = set_controller
        info_address = controller_topology[i]['address']
        #info.append(controller_topology[i]['backlog'])
        topo.controller_to_address[i] = info_address
    core.register_object('TopoHandler', topo)
