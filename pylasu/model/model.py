import ast
import inspect
from abc import ABC, abstractmethod
from typing import Optional, Callable

from .position import Position, Source


class internal_property(property):
    pass


def internal_properties(*props: str):
    def decorate(cls: type):
        cls.__internal_properties__ = [*Node.__internal_properties__, *props]
        return cls
    return decorate


class Origin(ABC):
    @internal_property
    @abstractmethod
    def position(self) -> Optional[Position]:
        pass

    @internal_property
    def source_text(self) -> Optional[str]:
        return None

    @internal_property
    def source(self) -> Optional[Source]:
        return self.position.source if self.position is not None else None


def is_internal_property_or_method(value):
    return isinstance(value, internal_property) or isinstance(value, Callable)


class Node(Origin, ast.AST):
    origin: Optional[Origin] = None
    parent: Optional["Node"] = None
    position_override: Optional[Position] = None
    __internal_properties__ = ["origin", "parent", "position"]

    def __init__(self, origin: Optional[Origin] = None, parent: Optional["Node"] = None,
                 position_override: Optional[Position] = None):
        self.origin = origin
        self.parent = parent
        self.position_override = position_override

    def with_origin(self, origin: Optional[Origin]):
        self.origin = origin
        return self

    def with_parent(self, parent: Optional["Node"]):
        self.parent = parent
        return self

    def with_position(self, position: Optional[Position]):
        self.position = position
        return self

    @internal_property
    def position(self) -> Optional[Position]:
        return self.position_override if self.position_override is not None\
            else self.origin.position if self.origin is not None else None

    @position.setter
    def position(self, position: Optional[Position]):
        self.position_override = position

    @internal_property
    def source_text(self) -> Optional[str]:
        return self.origin.source_text if self.origin is not None else None

    @internal_property
    def source(self) -> Optional[Source]:
        return self.origin.source if self.origin is not None else None

    @internal_property
    def properties(self):
        return ((name, getattr(self, name)) for name in dir(self)
                if not name.startswith('_')
                and name not in self.__internal_properties__
                and name not in [n for n, v in inspect.getmembers(type(self), is_internal_property_or_method)])

    @internal_property
    def _fields(self):
        yield from (name for name, _ in self.properties)

    @internal_property
    def node_type(self):
        return type(self)
