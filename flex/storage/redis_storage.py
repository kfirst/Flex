'''
Created on 2013-5-12

@author: kfirst
'''

import redis
from flex.base.module import Module
from flex.base.exception import IllegalKeyException
from flex.core import core
from flex.model.device import Device
from flex.model.packet import Packet, StoragePacketContent
from flex.base.handler import PacketHandler
import threading, Queue


class RedisStorage(Module, PacketHandler):

    SET = 1
    SADD = 2
    SADD_MULTI = 3

    def __init__(self, servers):
        self._myself = core.myself.get_self_controller()
        self._packet = Packet(Packet.STORAGE, StoragePacketContent(None, None, None))
        self._packet.src = self._myself
        self._handlers = {}
        self._keys_need_notify = Queue.Queue()
        self._pool = redis.ConnectionPool()
        self._num = len(servers)
        self._redises = [self._create_redis(server, port, self._pool)
                for server, port in servers]

    def start(self):
        core.forwarding.register_handler(Packet.STORAGE, self)
        self._start_thread()

    def _create_redis(self, server, port, pool):
        return redis.StrictRedis(host = server, port = port, connection_pool = pool)

    def _get_redis(self, key):
        num = hash(key) % self._num
        return self._redises[num]

    def _check_key(self, key):
        if key.startswith('#'):
            raise IllegalKeyException('Key could NOT start with _')

    def get(self, key):
        return self._get_redis(key).get(key)

    def set(self, key, value):
        self._check_key(key)
        redis = self._get_redis(key)
        ret = redis.set(key, value)
        self._keys_need_notify.put((key, value, redis, self.SET))
        return ret

    def sget(self, key):
        return self._get_redis(key).smembers(key)

    def sadd(self, key, value):
        self._check_key(key)
        redis = self._get_redis(key)
        ret = redis.sadd(key, value)
        self._keys_need_notify.put((key, value, redis, self.SADD))
        return ret

    def sadd_multi(self, key, values):
        self._check_key(key)
        redis = self._get_redis(key)
        pipe = redis.pipeline()
        for value in values:
            pipe.sadd(key, value)
        ret = pipe.execute()
        self._keys_need_notify.put((key, values, redis, self.SADD_MULTI))
        return ret

    def _start_thread(self):
        thread = threading.Thread(target = self._schedule)
        thread.setDaemon(True)
        thread.start()

    def _schedule(self):
        while 1:
            key, value, redis, type = self._keys_need_notify.get()
            listeners = redis.smembers('_%s' % (key))
            if listeners is not None:
                for listener, listen_myself in listeners:
                    if listener == self._myself.get_id() and not listen_myself:
                        continue
                    self._send_packet(listener, key, value, type)

    def _send_packet(self, listener, key, value, type):
        dst = Device.deserialize(listener)
        packet = self._packet
        packet.dst = dst
        packet.content.key = key
        packet.content.value = value
        packet.content.type = type
        core.forwarding.forward(self._packet)

    def listen(self, key, storage_handler, listen_myself = False):
        try:
            self._handlers[key].add(storage_handler)
        except KeyError:
            self._handlers[key] = set(storage_handler)
        self._get_redis(key).sadd('_%s' % key, (self._myself.serialize(), listen_myself))

    def handle_packet(self, packet):
        key = packet.content.key
        value = packet.content.value
        type = packet.content.type
        try:
            handlers = self._handlers[key]
            for handler in handlers:
                handler.handle(key, value, type)
        except KeyError:
            pass
