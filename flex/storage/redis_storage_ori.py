'''
Created on 2013-5-12

@author: kfirst
'''

import redis
from flex.core import core
from flex.model.device import Device
from flex.model.packet import Packet, StoragePacketContent
from flex.base.handler import PacketHandler
import cPickle
from flex.storage.storage import Storage

logger = core.get_logger()


class RedisStorage(Storage, PacketHandler):

    def __init__(self, servers):
        self._myself = core.myself.get_self_controller()
        self._key_handlers = {}
        self._domain_handlers = {}
        self._num = len(servers)
        self._redises = [redis.Redis(host = server, port = port)
                for server, port in servers]

    def start(self):
        core.forwarding.register_handler(Packet.STORAGE, self)

    def _get_redis(self, key):
        num = hash(key) % self._num
        return self._redises[num]

#    def _check_key(self, key):
#        if key.startswith('@') or key.startswith('#'):
#            raise IllegalKeyException('Key could NOT start with @, #')

    def _make_name(self, key, domain):
        return '%s:%s' % (domain, key)

    def _data_to_string(self, data):
        return cPickle.dumps(data, cPickle.HIGHEST_PROTOCOL)

    def _string_to_data(self, string):
        if string is None:
            return None
        return cPickle.loads(string)

    def get(self, key, domain = 'default'):
        name = self._make_name(key, domain)
        value = self._get_redis(name).get(name)
        return self._string_to_data(value)

    def set(self, key, value, domain = 'default'):
        name = self._make_name(key, domain)
        redis = self._get_redis(name)
        ret = redis.set(name, self._data_to_string(value))
        self._notify(key, value, domain, self.SET)
        return ret

    def delete(self, key, domain = 'default'):
        name = self._make_name(key, domain)
        redis = self._get_redis(name)
        ret = redis.delete(name)
        self._notify(key, None, domain, self.DELETE)
        return ret

    def sget(self, key, domain = 'default'):
        name = self._make_name(key, domain)
        values = self._get_redis(name).smembers(name)
        return set([self._string_to_data(value) for value in values])

    def sadd(self, key, value, domain = 'default'):
        name = self._make_name(key, domain)
        redis = self._get_redis(name)
        ret = redis.sadd(name, self._data_to_string(value))
        self._notify(key, value, domain, self.SADD)
        return ret

    def sremove(self, key, value, domain = 'default'):
        name = self._make_name(key, domain)
        redis = self._get_redis(name)
        ret = redis.srem(name, self._data_to_string(value))
        self._notify(key, value, domain, self.SREMOVE)
        return ret

    def sadd_multi(self, key, values, domain = 'default'):
        name = self._make_name(key, domain)
        redis = self._get_redis(name)
        pipe = redis.pipeline()
        for value in values:
            pipe.sadd(name, self._data_to_string(value))
        ret = pipe.execute()
        self._notify(key, values, domain, self.SADD_MULTI)
        return ret

    def _notify(self, key, value, domain, type):
#        self._queue.put((key, value, domain, type))
        self._notify_domain(key, value, domain, type)
        self._notify_key(key, value, domain, type)

    def _notify_domain(self, key, value, domain, type):
        listeners = self._get_redis(domain).smembers('#' + domain)
        listeners = [self._string_to_data(listener) for listener in listeners]
        for listener, listen_myself in listeners:
            if listener == self._myself.get_id() and not listen_myself:
                continue
            self._send_packet(listener, key, value, domain, type)

    def _notify_key(self, key, value, domain, type):
        name = self._make_name(key, domain)
        listeners = self._get_redis(name).smembers('@' + name)
        listeners = [self._string_to_data(listener) for listener in listeners]
        for listener, listen_myself in listeners:
            if listener == self._myself.get_id() and not listen_myself:
                continue
            self._send_packet(listener, key, value, domain, type)

    def _send_packet(self, listener, key, value, domain, type):
        packet = Packet(Packet.STORAGE, StoragePacketContent([(key, value, domain, type)]))
        packet.src = self._myself
        packet.dst = Device.deserialize(listener)
        core.forwarding.forward(packet)

    def listen_key(self, storage_handler, key, domain = 'default', listen_myself = False):
        name = self._make_name(key, domain)
        try:
            self._key_handlers[name].add(storage_handler)
        except KeyError:
            self._key_handlers[name] = set([storage_handler])
        redis = self._get_redis(name)
        redis.sadd('@' + name, self._data_to_string((self._myself.serialize(), listen_myself)))
        if not listen_myself:
            redis.srem('@' + name, self._data_to_string((self._myself.serialize(), True)))

    def listen_domain(self, storage_handler, domain, listen_myself = False):
        try:
            self._domain_handlers[domain].add(storage_handler)
        except KeyError:
            self._domain_handlers[domain] = set([storage_handler])
        redis = self._get_redis(domain)
        redis.sadd('#' + domain, self._data_to_string((self._myself.serialize(), listen_myself)))
        if not listen_myself:
            redis.srem('#' + domain, self._data_to_string((self._myself.serialize(), True)))

    def handle_packet(self, packet):
#        logger.debug('Storage packet received')
        tasks = packet.content.tasks
        for key, value, domain, type in tasks:
            try:
                handlers = self._domain_handlers[domain]
                for handler in handlers:
                    handler.handle_storage(key, value, domain, type)
            except KeyError:
                pass
            try:
                handlers = self._key_handlers[self._make_name(key, domain)]
                for handler in handlers:
                    handler.handle_storage(key, value, domain, type)
            except KeyError:
                pass
