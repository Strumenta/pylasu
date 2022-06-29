import ast
import inspect
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Callable

from .position import Position, Source


class internal_property(property):
    pass


class Origin(ABC):
    @property
    @abstractmethod
    def position(self) -> Optional[Position]:
        pass

    @property
    def source_text(self) -> Optional[str]:
        return None

    @property
    def source(self) -> Optional[Source]:
        return self.position.source if self.position is not None else None


def is_internal_property_or_method(value):
    return isinstance(value, internal_property) or isinstance(value, Callable)


@dataclass
class Node(Origin, ast.AST):
    origin: Optional[Origin] = None
    parent: Optional["Node"] = None
    position: Optional[Position] = None

    def __post_init__(self):
        if isinstance(self.origin, property):
            self.origin = None
        if isinstance(self.parent, property):
            self.parent = None

    @internal_property
    def origin(self) -> Optional[Origin]:
        return self._origin

    @origin.setter
    def origin(self, origin: Origin):
        self._origin = origin

    @internal_property
    def parent(self) -> Optional["Node"]:
        return self._parent

    @parent.setter
    def parent(self, parent: "Node"):
        self._parent = parent

    def with_parent(self, parent: "Node"):
        self.parent = parent
        return self

    @internal_property
    def position(self) -> Position:
        return self._position if self._position is not None\
            else self.origin.position if self.origin is not None else None

    @position.setter
    def position(self, position: Position):
        self._position = position

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
                and name not in [n for n, v in inspect.getmembers(type(self), is_internal_property_or_method)])

    @internal_property
    def _fields(self):
        yield from (name for name, _ in self.properties)

    @internal_property
    def node_type(self):
        return type(self)
