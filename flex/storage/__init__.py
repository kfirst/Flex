from flex.core import core
from flex.storage.local_storage import LocalStorage
from flex.storage.redis_storage_ori import RedisStorage

def launch():
    storages_config = core.config.get('module.storage')
    redis = None
    local = None
    for name, parameters in storages_config.items():
        if parameters:
            if redis is None:
                redis = RedisStorage(**parameters)
            core.register_object(name, redis)
        else:
            if local is None:
                local = LocalStorage()
            core.register_object(name, local)
