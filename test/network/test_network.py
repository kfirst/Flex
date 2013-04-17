'''
Created on 2013-4-17

@author: kfirst
'''

from flex.core import core
import time
from flex.base.handler import DataHandler

class Handler(DataHandler):
    def handle(self, data):
        print 'receive data ' + str(data)

core.set_config_path('../config')
core.start()
network = core.network
network.register_data_handler(Handler())

network.send(("127.0.0.1", 12210), 'test1')
network.send(("127.0.0.1", 12210), 'test2')

time.sleep(1)

network.send(("127.0.0.1", 12210), 'test3')
network.send(("127.0.0.1", 12210), 'test4')

time.sleep(1)
