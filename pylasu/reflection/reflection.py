import typing
from enum import Enum, EnumMeta
from typing import Callable


def get_type_annotations(cls: type):
    if hasattr(typing, "get_type_hints"):
        # https://peps.python.org/pep-0563/
        return typing.get_type_hints(cls)
    else:
        try:
            # On Python 3.10+
            import inspect

            if hasattr(inspect, "get_annotations"):
                return inspect.get_annotations(cls)
            elif hasattr(inspect, "getannotations"):
                return inspect.getannotations(cls)
        except ModuleNotFoundError:
            pass
        if isinstance(cls, type):
            return cls.__dict__.get("__annotations__", {})
        else:
            return getattr(cls, "__annotations__", {})


def get_type_origin(tp):
    origin = None
    if hasattr(typing, "get_origin"):
        origin = typing.get_origin(tp)
    elif hasattr(tp, "__origin__"):
        origin = tp.__origin__
    elif tp is typing.Generic:
        origin = typing.Generic
    return origin or (tp if isinstance(tp, type) else None)


def is_enum_type(attr_type):
    return isinstance(attr_type, EnumMeta) and issubclass(attr_type, Enum)


def is_sequence_type(attr_type):
    return isinstance(get_type_origin(attr_type), type) and issubclass(
        get_type_origin(attr_type), typing.Sequence
    )


def get_type_arguments(tp):
    if hasattr(typing, "get_args"):
        return typing.get_args(tp)
    elif hasattr(tp, "__args__"):
        res = tp.__args__
        if get_type_origin(tp) is Callable and res[0] is not Ellipsis:
            res = (list(res[:-1]), res[-1])
        return res
    return ()
