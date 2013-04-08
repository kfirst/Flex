'''
Created on 2013-4-8

@author: fzm
'''
from flex.core import core
import time

core.set_config_path('../../config')
core.start()
cpf = core.control_packet_forwarding


print cpf.self_controller
self_id = cpf.self_id

controller = core.topology._controllers[self_id]

print controller
