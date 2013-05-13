from flex.core import core
from flex.storage.local_storage import LocalStorage
from flex.storage.redis_storage import RedisStorage

def launch():
    storages = core.config.get('module.storage')
    for name, parameters in storages.items():
        if parameters:
            core.register_object(name, RedisStorage(**parameters))
        else:
            core.register_object(name, LocalStorage())
