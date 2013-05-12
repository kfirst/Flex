from flex.core import core
from flex.storage.storage import Storage

def launch():
    storages = core.config.get('module.storage')
    for name, parameters in storages.items():
        core.register_object(name, Storage(**parameters))
