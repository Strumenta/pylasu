import inspect
from abc import ABC, abstractmethod, ABCMeta
from dataclasses import Field, MISSING, dataclass, field
from typing import Optional, Callable, List, Union

from .naming import ReferenceByName
from .position import Position, Source
from .reflection import Multiplicity, PropertyDescription
from ..reflection import getannotations, get_type_arguments, is_sequence_type
from ..reflection.reflection import get_type_origin


class internal_property(property):
    pass


def internal_properties(*props: str):
    def decorate(cls: type):
        cls.__internal_properties__ = (
            getattr(cls, "__internal_properties__", []) + [*Node.__internal_properties__, *props])
        return cls
    return decorate


class InternalField(Field):
    pass


def internal_field(
        *, default=MISSING, default_factory=MISSING, init=True, repr=True, hash=None, compare=True, metadata=None,
        kw_only=False):
    """Return an object to identify internal dataclass fields. The arguments are the same as dataclasses.field."""

    if default is not MISSING and default_factory is not MISSING:
        raise ValueError('cannot specify both default and default_factory')
    try:
        # Python 3.10+
        return InternalField(default, default_factory, init, repr, hash, compare, metadata, kw_only)
    except TypeError:
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


def provides_nodes(decl_type):
    if get_type_origin(decl_type) is Union:
        provides = None
        for tp in get_type_arguments(decl_type):
            if tp is type(None):
                continue
            arg_provides = provides_nodes(tp)
            if provides is None:
                provides = arg_provides
            elif provides != arg_provides:
                raise Exception(f"Type {decl_type} mixes nodes and non-nodes")
        return provides
    else:
        return isinstance(decl_type, type) and issubclass(decl_type, Node)


def get_only_type_arg(decl_type):
    """If decl_type has a single type argument, return it, otherwise return None"""
    type_args = get_type_arguments(decl_type)
    if len(type_args) == 1:
        return type_args[0]
    else:
        return None


def process_annotated_property(name, decl_type, known_property_names):
    multiplicity = Multiplicity.SINGULAR
    is_reference = False
    if get_type_origin(decl_type) is ReferenceByName:
        decl_type = get_only_type_arg(decl_type) or decl_type
        is_reference = True
    if is_sequence_type(decl_type):
        decl_type = get_only_type_arg(decl_type) or decl_type
        multiplicity = Multiplicity.MANY
    if get_type_origin(decl_type) is Union:
        type_args = get_type_arguments(decl_type)
        if len(type_args) == 1:
            decl_type = type_args[0]
        elif len(type_args) == 2:
            if type_args[0] is type(None):
                decl_type = type_args[1]
            elif type_args[1] is type(None):
                decl_type = type_args[0]
            else:
                raise Exception(f"Unsupported feature {name} of type {decl_type}")
            if multiplicity == Multiplicity.SINGULAR:
                multiplicity = Multiplicity.OPTIONAL
        else:
            raise Exception(f"Unsupported feature {name} of type {decl_type}")
    if not isinstance(decl_type, type):
        raise Exception(f"Unsupported feature {name} of type {decl_type}")
    is_containment = provides_nodes(decl_type) and not is_reference
    known_property_names.add(name)
    return PropertyDescription(name, decl_type, is_containment, is_reference, multiplicity)


class Concept(ABCMeta):

    def __init__(cls, what, bases=None, dict=None):
        super().__init__(what, bases, dict)
        cls.__internal_properties__ = []
        for base in bases:
            if hasattr(base, "__internal_properties__"):
                cls.__internal_properties__.extend(base.__internal_properties__)
        if not cls.__internal_properties__:
            cls.__internal_properties__ = ["origin", "destination", "parent", "position", "position_override"]
        cls.__internal_properties__.extend([n for n, v in inspect.getmembers(cls, is_internal_property_or_method)])

    @property
    def node_properties(cls):
        names = set()
        for cl in cls.__mro__:
            yield from cls._direct_node_properties(cl, names)

    def _direct_node_properties(cls, cl, known_property_names):
        anns = getannotations(cl)
        if not anns:
            return
        for name in anns:
            if name not in known_property_names and cls.is_node_property(name):
                yield process_annotated_property(name, anns[name], known_property_names)
        for name in dir(cl):
            if name not in known_property_names and cls.is_node_property(name):
                known_property_names.add(name)
                yield PropertyDescription(name, None, False, False)

    def is_node_property(cls, name):
        return not name.startswith('_') and name not in cls.__internal_properties__


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
        return (PropertyDescription(p.name, p.type,
                                    is_containment=p.is_containment, is_reference=p.is_reference,
                                    multiplicity=p.multiplicity, value=getattr(self, p.name))
                for p in self.__class__.node_properties)

    @internal_property
    def _fields(self):
        yield from (name for name, _ in self.properties)

    @internal_property
    def node_type(self):
        return type(self)


def concept_of(node):
    properties = dir(node)
    if "__concept__" in properties:
        node_type = node.__concept__
    elif "node_type" in properties:
        node_type = node.node_type
    else:
        node_type = type(node)
    if isinstance(node_type, Concept):
        return node_type
    else:
        raise Exception(f"Not a concept: {node_type} of {node}")
