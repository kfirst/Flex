# encoding: utf-8
'''
Created on 2013-3-19

@author: kfirst
'''

from flex.base.module import Module

class Core(Module):

    def __init__(self):
        self._components = {}
        self._config_path = '../config'

    def set_config_path(self, config_path):
        self._config_path = config_path

    def start(self):
        from flex import config
        config.launch(self._config_path)
        from flex import logger
        logger.launch()
        from flex import event
        event.launch()
        components = self.config.get('module.core.module', [])
        for component in components:
            component_class = __import__(component, fromlist = [''])
            component_class.launch()
        for component in self._components:
            self._components[component].start()

    def register_component(self, component_class, *args, **kw):
        name = component_class.__name__.lower()
        if name in self._components:
            raise AttributeError('Attribute [' + name + '] already exists in Core!')
        obj = component_class(*args, **kw)
        self._components[name] = obj

    def register_object(self, name, obj):
        name = name.lower()
        if name in self._components:
            raise AttributeError('Attribute [' + name + '] already exists in Core!')
        self._components[name] = obj

    def get_logger(self, name = None):
        return self.logger_generator.get_logger(name, 1)

    def __getattr__(self, name):
        try:
            return self._components[name]
        except KeyError:
            raise AttributeError('Attribute [' + name + '] is not found in Core!')


core = Core()


if __name__ == '__main__':
    from flex.core import core
    core.start()
    logger = core.get_logger()
    logger.warning('test')
    print core.network._myself
