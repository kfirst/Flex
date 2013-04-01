from flex.logger.logger_parser import LoggerParser
from flex.core import core

def launch():
    logger_parser = LoggerParser()
    logger_generator = logger_parser.parse(core.config)
    core.register_object('logger', logger_generator)
