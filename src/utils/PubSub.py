import time
from threading import Thread, Event
from typing import Dict

from redis import StrictRedis

from src.utils.injection.decorator import inject


class PubSub:
    """
    A redis based PubSub pattern implementation for many-to-many communication.
    This class is intended for communication in asynchronous and multi-threaded
    applications (note that unix threads do not have shared memory). It does not
    provide guarantee of sequential execution, but rather allows several subprocesses
    to process same raw_data. Processes must NOT alter raw_data as it is sent by reference
    """

    @inject
    def __init__(self, redis: StrictRedis = None):
        """
        Initialize redis instance

        :param Redis redis: redis instance
        """
        assert redis is not None, "Redis must be initialized"
        self.redis = redis

    def publish(self, channel: str, message: object):
        """
        Publish raw_data to redis

        :param str channel: channel name
        :param object message: raw_data to be published
        """
        self.redis.publish(channel, message)

    def subscribe(self, channel: str, callback: callable, daemon: bool = True) -> Event:
        """
        Subscribe to a channel

        :param str channel: channel name
        :param callable callback: a callback to be executed on receiving a message
        :param bool daemon: run subscriber in daemon mode

        :return: returns callback id in the queue
        :int:
        """

        event = Event()
        Thread(target=self._subscribe_loop, args=(channel, callback, event), daemon=daemon).start()
        return event

    def unsubscribe(self, event: Event):
        """
        Unsubscribe from channel

        :param event: event associated with subscriber instance
        :return:
        """
        event.set()

    def _subscribe_loop(self, channel: str, callback: callable, event: Event):
        redis_pubsub = self.redis.pubsub()
        redis_pubsub.subscribe(channel)
        for message in redis_pubsub.listen():
            if event.is_set():
                break

            if message['type'] != 'message':
                continue

            self._on_receive(message, callback)

        redis_pubsub.unsubscribe(channel)

    @classmethod
    def _on_receive(cls, message: dict, callback: callable):
        callback(message['data'])
