from flex.core import core
from flex.config.config import Config

def launch(path):
    core.register_component(Config, path)
