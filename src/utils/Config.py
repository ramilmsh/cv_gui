import json
from threading import Lock

from redis import Redis

from src.utils.injection.decorator import inject


class Config(dict):
    DEFAULT_CONFIG = {
        "system": "macos"
    }

    @inject
    def __init__(self, redis: Redis = None, **kwargs):
        super(Config, self).__init__(kwargs)
        self.redis = redis
        self.config = {}

        self._load_config()
        self._data_lock = Lock()

    def reset(self):
        self.redis.flushall(asynchronous=False)
        self._update_keys(Config.DEFAULT_CONFIG)

    def _update_keys(self, config: dict):
        for key in config:
            self[key] = config[key]

    def _load_config(self):
        for key in self.redis.keys():
            super(Config, self).__setitem__(json.loads(key),
                                            json.loads(self.redis.get(key)))

    def __getitem__(self, item):
        with self._data_lock:
            data = super(Config, self).__getitem__(item)
        return data

    def __setitem__(self, key, value: [list, dict, str, int, float]):
        with self._data_lock:
            super(Config, self).__setitem__(key, value)
            if type(value) == list or type(value) == dict:
                value = json.dumps(value)
            self.redis.set(key, value)
