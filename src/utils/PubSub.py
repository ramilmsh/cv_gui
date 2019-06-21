import time
from redis import StrictRedis
from queue import PriorityQueue
from threading import Thread, Lock

from src.utils.OrderedHashSet import OrderedHashSet


class PubSub:
    """
    A redis based PubSub pattern implementation for many-to-many communication.
    This class is intended for communication in asynchronous and multi-threaded
    applications (note that unix threads do not have shared memory). It does not
    provide guarantee of sequential execution, but rather allows several subprocesses
    to process same data. Processes must NOT alter data as it is sent by reference
    """
    SINGLETON = None

    def __init__(self):
        """
        Initialize redis instance

        :param dict args: positional arguments (passed on to redis instance)
        :param dict kwargs: key-word arguments (passed on to redis instance)
        """
        self.redis = StrictRedis()
        self.subscribers = {}
        self.subscribers_lock = Lock()
        self.threads = {}
        PubSub.SINGLETON = self

    def publish(self, channel: str, message: object):
        """
        Publish data to redis

        :param str channel: channel name
        :param object message: data to be published
        """
        self.redis.publish(channel, message)

    def subscribe(self, channel: str, callback: callable) -> str:
        """
        Subscribe to a channel

        :param str channel: channel name
        :param callable callback: a callback to be executed on receiving a message

        :return: returns callback id in the queue
        :int:
        """
        if channel not in self.subscribers:
            self.subscribers[channel] = OrderedHashSet()

        _id = self.subscribers[channel].append(callback)

        if channel not in self.threads or not self.threads[channel].is_alive():
            self.threads[channel] = Thread(
                target=self._subscribe_loop, args=(channel, ), daemon=True)
            self.threads[channel].start()

        return _id

    def unsubscribe(self, channel: str, id: str):
        if self.subscribers[channel] is None:
            return

        with self.subscribers_lock:
            del self.subscribers[channel][id]
        if len(self.subscribers[channel]) == 0:
            self.redis.publish(channel, 'done')

    @classmethod
    def get_instance(cls):
        if PubSub.SINGLETON is None:
            PubSub.SINGLETON = PubSub()
        return PubSub.SINGLETON

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

    def _on_receive(self, channel: str, message: object, callback: callable):
        callback(message['data'])
