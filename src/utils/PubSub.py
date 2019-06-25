import time
from typing import Dict

import numpy as np
from redis import StrictRedis
from threading import Thread, Lock

from src.utils.injection.decorator import inject
from src.utils.OrderedHashSet import OrderedHashSet


class PubSub:
    """
    A redis based PubSub pattern implementation for many-to-many communication.
    This class is intended for communication in asynchronous and multi-threaded
    applications (note that unix threads do not have shared memory). It does not
    provide guarantee of sequential execution, but rather allows several subprocesses
    to process same data. Processes must NOT alter data as it is sent by reference
    """

    @inject
    def __init__(self, redis: StrictRedis = None):
        """
        Initialize redis instance

        :param Redis redis: redis instance
        """
        assert redis is not None, "Redis must be initialized"
        self.redis = redis
        self.subscribers = {}  # type: Dict[str, OrderedHashSet]
        self.subscribers_lock = Lock()
        self.threads = {}

    def publish(self, channel: str, message: object):
        """
        Publish data to redis

        :param str channel: channel name
        :param object message: data to be published
        """
        self.redis.publish(channel, message)

    def subscribe(self, channel: str, callback: callable, daemon: bool = True) -> int:
        """
        Subscribe to a channel

        :param str channel: channel name
        :param callable callback: a callback to be executed on receiving a message
        :param bool daemon: run subscriber in daemon mode

        :return: returns callback id in the queue
        :int:
        """
        if channel not in self.subscribers:
            self.subscribers[channel] = OrderedHashSet()

        with self.subscribers_lock:
            _id = self.subscribers[channel].append(callback)

        if channel not in self.threads or not self.threads[channel].is_alive():
            self.threads[channel] = Thread(
                target=self._subscribe_loop, args=(channel,), daemon=daemon)
            self.threads[channel].start()
        return _id

    def unsubscribe(self, channel: str, _id: int):
        if channel not in self.subscribers or _id not in self.subscribers[channel]:
            return

        with self.subscribers_lock:
            del self.subscribers[channel][_id]
        if len(self.subscribers[channel]) == 0:
            self.redis.publish(channel, 'done')

    def _subscribe_loop(self, channel: str):
        redis_pubsub = self.redis.pubsub()
        redis_pubsub.subscribe(channel)

        for message in redis_pubsub.listen():

            if message['type'] != 'message':
                continue

            if len(self.subscribers[channel]) == 0:
                break

            with self.subscribers_lock:
                for callback in self.subscribers[channel].values():
                    self._on_receive(channel, message, callback)
        redis_pubsub.unsubscribe(channel)

    def _on_receive(self, channel: str, message: dict, callback: callable):
        callback(message['data'])
