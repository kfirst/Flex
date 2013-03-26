'''
Created on 2013-3-20

@author: fzm
'''
class FindHopOfController(object):
    
    def __init__(self):
        #self.controller2controller = {}
        pass
    def find_hop(self, controller_id, target_id, topo_of_controller):
        controller_step = {}
        for i in topo_of_controller:
            controller_step[i] = 0
        controller_step[controller_id] = 1;
        step = 1
        controller_set = topo_of_controller[controller_id]
        while 1==1:
            step = step + 1
            controller_step_temp = set()
            for i in controller_set:
                controller_step[i] = step
            if target_id in controller_set:
                break
            if len(controller_set) == 0:
                return None
            for i in controller_set:
                for j in topo_of_controller[i]:
                    if controller_step[j] == 0:
                        controller_step_temp.add(j)
            controller_set = controller_step_temp
        #回溯
        controller_temp = target_id
        while 1==1:
            if controller_step[controller_temp] == 2:
                return controller_temp
            for i in topo_of_controller[controller_temp]:
                if controller_step[i] == controller_step[controller_temp] - 1:
                    controller_temp = i;
                    break
                    
            
            
            
            
                
            
    
    