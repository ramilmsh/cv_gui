from functools import wraps
import inspect


class Bindings:
    """
    Existing bindings that can beinjected
    """
    _bindings = ['Redis', 'PubSub', 'Config']
    _singletons = {}

    @classmethod
    def get_instance(cls, annotation):
        """
        Get instance of a singleton

        :param annotation: requested class
        :return:
        """
        if annotation.__name__ in cls._bindings:
            if annotation not in cls._singletons:
                cls._singletons[annotation] = annotation()
            return cls._singletons[annotation]

        return None
    
    @classmethod
    def binding_available(cls, annotation):
        """
        Check if a kwarg is of an injectable class

        :param annotation: requested class
        :return:
        """
        if not hasattr(annotation, '__name__'):
            return False
        return annotation.__name__ in cls._bindings


def inject(function):
    """
    A function decorator for injecting project-wide dependencies

    :param function: function to be injected
    :return:
    """

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
