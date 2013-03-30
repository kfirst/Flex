# encoding: utf-8
'''
解析配置文件中有关log的部分。
Created on 2013-3-19

@author: kfirst
'''

import logging
from flex.logger.logger_generator import LoggerGenerator

class LoggerParser(object):

    DEFAULT_LEVEL = 'WARNING'
    DEFAULR_FORMAT = '%(levelname)-10s[%(name)-s]: %(message)s'
    DEFAULT_HANDLER = {'StreamHandler':[]}

    def __init__(self):
        self._handlers = []
        self._formatter = logging.Formatter

    def parse(self, config):
        level_config = config.get('module.log.level', self.DEFAULT_LEVEL)
        self._level = self._parse_level(level_config)
        formatter_config = config.get('module.log.format', self.DEFAULR_FORMAT)
        self._formatter = self._parse_formater(formatter_config)
        handler_config = config.get('module.log.handler', self.DEFAULT_HANDLER)
        self._handlers = self._parse_handler(handler_config)
        for handler in self._handlers:
            handler.setFormatter(self._formatter)
        return LoggerGenerator(self._level, self._handlers)

    def _parse_level(self, value):
        return getattr(logging, value)

    def _parse_handler(self, value):
        handler = []
        for k in value:
            handler.append(getattr(logging, k)(*value[k]))
        return handler

    def _parse_formater(self, value):
        return logging.Formatter(value)


if __name__ == '__main__':
    from flex.config.config import Config
    config = Config('../../config')
    parser = LoggerParser()
    log = parser.parse(config)
    l = log.get_logger()
    l.warning('test error')
