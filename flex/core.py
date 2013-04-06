# encoding: utf-8
'''
Created on 2013-3-19

@author: kfirst
'''

from flex.base.module import Module

# import inspect, os, sys
# _path = inspect.stack()[0][1]
# _path = _path[0:_path.rindex(os.sep)]
# sys.path.append(os.path.abspath(_path))

class Core(Module):

    def __init__(self):
        self.version()
        self._components = {}
        self._component_names = []
        self._config_path = '../config'

    def version(self):
        print 'Flex 0.0.1'

    def set_config_path(self, config_path):
        self._config_path = config_path

    def start(self):
        from flex import config
        config.launch(self._config_path)
        from flex import logger
        logger.launch()
        from flex import event
        event.launch()
        from flex import myself
        myself.launch()

        self._logger = self.get_logger()
        components = self.config.get('module.core.module', [])
        for component in components:
            self._logger.debug('Lanch ' + component)
            component_class = __import__(component, fromlist = [''])
            component_class.launch()
        for name in self._component_names:
            self._logger.debug('Start ' + name)
            self._components[name].start()

    def register_component(self, component_class, *args, **kw):
        name = component_class.__name__.lower()
        if name in self._components:
            raise AttributeError('Attribute [' + name + '] already exists in Core!')
        obj = component_class(*args, **kw)
        self._components[name] = obj
        self._component_names.append(name)

    def register_object(self, name, obj):
        name = name.lower()
        if name in self._components:
            raise AttributeError('Attribute [' + name + '] already exists in Core!')
        self._components[name] = obj
        self._component_names.append(name)

    def get_logger(self, name = None):
        return self.logger.get_logger(name, 1)

    def __getattr__(self, name):
        name = name.lower()
        try:
            return self._components[name]
        except KeyError:
            raise AttributeError('Attribute [' + name + '] is not found in Core!')


core = Core()
