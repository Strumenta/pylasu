from pylasu.model.model import Concept


def register_internal_property(cls, name):
    cls.__internal_properties__.append(name)
    for s in cls.__subclasses__():
        register_internal_property(s, name)


def extension_method(cls):
    """Installs the decorated function as an extension method on cls.
    See https://mail.python.org/pipermail/python-dev/2008-January/076194.html"""
    def decorator(func):
        name = func.__name__
        if name in cls.__dict__:
            raise Exception(f"{cls} already has a member called {name}")
        setattr(cls, name, func)
        if isinstance(cls, Concept):
            register_internal_property(cls, name)
        return func
    return decorator
