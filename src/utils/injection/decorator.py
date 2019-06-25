from functools import wraps
from enum import Enum
import inspect


class Bindings:
    _bindings = ['Redis', 'PubSub', 'Config']
    _singletons = {}

    @classmethod
    def get_instance(cls, annotation):
        if annotation.__name__ in cls._bindings:
            if annotation not in cls._singletons:
                cls._singletons[annotation] = annotation()
            return cls._singletons[annotation]

        return None
    
    @classmethod
    def binding_available(cls, annotation):
        if type(annotation) == list or type(annotation) == dict:
            return False
        return annotation.__name__ in cls._bindings


def inject(function):

    @wraps(function)
    def new_init(*args, **kwargs):
        injections = {}

        parameters = inspect.signature(function).parameters
        for param_name in parameters:
            param = parameters[param_name]
            if Bindings.binding_available(param.annotation):
                injections[param.name] = Bindings.get_instance(param.annotation)

        kwargs.update(injections)
        function(*args, **kwargs)
    
    return new_init
