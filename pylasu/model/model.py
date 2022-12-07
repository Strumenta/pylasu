import enum
import inspect
from abc import ABC, abstractmethod, ABCMeta
from dataclasses import Field, MISSING, dataclass, field
from typing import Optional, Callable, List, Generator

from .position import Position, Source
from ..reflection import getannotations


class internal_property(property):
    pass


def internal_properties(*props: str):
    def decorate(cls: type):
        cls.__internal_properties__ = [*Node.__internal_properties__, *props]
        return cls
    return decorate


class InternalField(Field):
    pass


def internal_field(
        *, default=MISSING, default_factory=MISSING, init=True, repr=True, hash=None, compare=True, metadata=None):
    """Return an object to identify internal dataclass fields. The arguments are the same as dataclasses.field."""

    if default is not MISSING and default_factory is not MISSING:
        raise ValueError('cannot specify both default and default_factory')
    return InternalField(default, default_factory, init, repr, hash, compare, metadata)


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


@dataclass
class CompositeOrigin(Origin):
    elements: List[Origin] = field(default_factory=list)
    position: Optional[Position] = None
    source_text: Optional[str] = None


class Destination(ABC):
    pass


@dataclass
class CompositeDestination(Destination):
    elements: List[Destination] = field(default_factory=list)


@dataclass
class TextFileDestination(Destination):
    position: Optional[Position] = None


def is_internal_property_or_method(value):
    return isinstance(value, internal_property) or isinstance(value, InternalField) or isinstance(value, Callable)


class Multiplicity(enum.Enum):
    OPTIONAL = 0
    SINGULAR = 1
    MANY = 2


@dataclass
class PropertyDescriptor:
    name: str
    provides_nodes: bool
    multiplicity: Multiplicity = Multiplicity.SINGULAR


class Concept(ABCMeta):

    def __init__(cls, what, bases=None, dict=None):
        super().__init__(what, bases, dict)
        cls.__internal_properties__ = ["origin", "destination", "parent", "position", "position_override"]

    @property
    def node_properties(cls):
        anns = getannotations(cls)
        names = set()
        for name in anns:
            if name not in names and cls.is_node_property(name):
                provides_nodes = False
                if name in anns:
                    provides_nodes = isinstance(anns[name], type) and issubclass(anns[name], Node)
                names.add(name)
                yield PropertyDescriptor(name, provides_nodes)
        for name in dir(cls):
            if name not in names and cls.is_node_property(name):
                names.add(name)
                yield PropertyDescriptor(name, False)

    def is_node_property(cls, name):
        return not name.startswith('_') \
               and name not in cls.__internal_properties__ \
               and name not in [n for n, v in inspect.getmembers(cls, is_internal_property_or_method)]


class Node(Origin, Destination, metaclass=Concept):
    origin: Optional[Origin] = None
    destination: Optional[Destination] = None
    parent: Optional["Node"] = None
    position_override: Optional[Position] = None

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
