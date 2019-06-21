from functools import wraps
from enum import Enum

from src.utils.PubSub import PubSub

class BINDINGS(Enum):
    PUBSUB = PubSub.get_instance()


def inject(function):

    @wraps(function)
    def new_init(*args, **kwargs):
        injections = {}

        for binding in BINDINGS:
            injections[binding.name.lower()] = binding.value

        kwargs.update(injections)
        function(*args, **kwargs)
    
    return new_init