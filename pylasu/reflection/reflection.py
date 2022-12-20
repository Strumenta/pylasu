import typing
from enum import EnumMeta, Enum
from typing import Callable


def getannotations(cls):
    import inspect
    try:  # On Python 3.10+
        return inspect.getannotations(cls)
    except AttributeError:
        if isinstance(cls, type):
            return cls.__dict__.get('__annotations__', None)
        else:
            return getattr(cls, '__annotations__', None)


def get_type_origin(tp):
    if hasattr(typing, "get_origin"):
        return typing.get_origin(tp)
    elif hasattr(tp, "__origin__"):
        return tp.__origin__
    elif tp is typing.Generic:
        return typing.Generic
    else:
        return None


def is_enum_type(attr_type):
    return isinstance(attr_type, EnumMeta) and issubclass(attr_type, Enum)


def is_sequence_type(attr_type):
    return isinstance(get_type_origin(attr_type), type) and \
        issubclass(get_type_origin(attr_type), typing.Sequence)


def get_type_arguments(tp):
    if hasattr(typing, "get_args"):
        return typing.get_args(tp)
    elif hasattr(tp, "__args__"):
        res = tp.__args__
        if get_type_origin(tp) is Callable and res[0] is not Ellipsis:
            res = (list(res[:-1]), res[-1])
        return res
    return ()
