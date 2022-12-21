import functools
from dataclasses import dataclass, field
from inspect import signature
from typing import Any, Dict, Callable, TypeVar, Generic, Optional, List, Set, Iterable, Type, Union

from pylasu.model import Node, Origin
from pylasu.model.errors import GenericErrorNode
from pylasu.model.model import PropertyDescriptor
from pylasu.transformation.generic_nodes import GenericNode
from pylasu.validation import Issue, IssueSeverity

Child = TypeVar('Child')
Output = TypeVar('Output', bound=Node)
Source = TypeVar('Source')
Target = TypeVar('Target')
node_factory_constructor_type = Callable[[Source, "ASTTransformer", "NodeFactory[Source, Output]"], Optional[Output]]


@dataclass
class PropertyRef:
    name: str

    def get(self, node: Node):
        return getattr(node, self.name)

    def set(self, node: Node, value):
        return setattr(node, self.name, value)


@dataclass
class NodeFactory(Generic[Source, Output]):
    constructor: node_factory_constructor_type
    children: Dict[str, "ChildNodeFactory[Source, Any, Any]"] = field(default_factory=dict)
    finalizer: Callable[[Source], None] = lambda _: None

    def with_child(
            self,
            getter: Union[Callable[[Source], Optional[Any]], PropertyRef],
            setter: Union[Callable[[Target, Optional[Child]], None], PropertyRef],
            name: Optional[str] = None,
            target_type: Optional[type] = None
    ) -> "NodeFactory[Source, Output]":
        if not name:
            name = setter.name
        if target_type:
            prefix = target_type.__qualname__ + "#"
        else:
            prefix = ""
        if isinstance(getter, PropertyRef):
            getter = getter.get
        if isinstance(setter, PropertyRef):
            setter = setter.set
        self.children[prefix + name] = ChildNodeFactory(prefix + name, getter, setter)
        return self


@dataclass
class ChildNodeFactory(Generic[Source, Target, Child]):
    name: str
    get: Callable[[Source], Optional[Any]]
    setter: Callable[[Target, Optional[Child]], None]

    def set(self, node: Target, child: Optional[Child]):
        try:
            self.setter(node, child)
        except Exception as e:
            raise Exception(f"{self.name} could not set child {child} of {node} using {self.setter}") from e


"""Sentinel value used to represent the information that a given property is not a child node."""
NO_CHILD_NODE = ChildNodeFactory("", lambda x: x, lambda _, __: None)


class ASTTransformer:
    issues: List[Issue] = []
    "Additional issues found during the transformation process."
    allow_generic_node: bool = True
    factories: Dict[type, NodeFactory]
    "Factories that map from source tree node to target tree node."
    known_classes: Dict[str, Set[type]]

    def __init__(self, allow_generic_node: bool = True):
        self.issues = []
        self.allow_generic_node = allow_generic_node
        self.factories = dict()
        self.known_classes = dict()

    def transform(self, source: Optional[Any], parent: Optional[Node] = None) -> Optional[Node]:
        if source is None:
            return None
        elif isinstance(source, Iterable):
            raise Exception(f"Mapping error: received collection when value was expected: {source}")
        factory = self.get_node_factory(type(source))
        if factory:
            node = self.make_node(factory, source)
            if not node:
                return None
            for pd in type(node).node_properties:
                self.process_child(source, node, pd, factory)
            factory.finalizer(node)
            node.parent = parent
        else:
            if self.allow_generic_node:
                origin = self.as_origin(source)
                node = GenericNode(parent).with_origin(origin)
                self.issues.append(
                    Issue.semantic(
                        f"Source node not mapped: {type(source).__qualname__}",
                        IssueSeverity.INFO,
                        origin.position if origin else None))
            else:
                raise Exception(f"Unable to translate node {source} (${type(source)})")
        return node

    def process_child(self, source, node, pd, factory):
        child_key = type(node).__qualname__ + "#" + pd.name
        if child_key in factory.children:
            child_node_factory = factory.children[child_key]
        elif pd.name in factory.children:
            child_node_factory = factory.children[pd.name]
        else:
            child_node_factory = None
        if child_node_factory:
            if child_node_factory != NO_CHILD_NODE:
                self.set_child(child_node_factory, source, node, pd)
        else:
            # TODO should we support @Mapped?
            factory.children[child_key] = NO_CHILD_NODE

    def as_origin(self, source: Any) -> Optional[Origin]:
        return source if isinstance(source, Origin) else None

    def set_child(self, child_node_factory: ChildNodeFactory, source: Any, node: Node, pd: PropertyDescriptor):
        src = child_node_factory.get(self.get_source(node, source))
        if pd.multiple():
            child = [self.transform(it, node) for it in src or [] if it is not None]
        else:
            child = self.transform(src, node)
        try:
            child_node_factory.set(node, child)
        except Exception as e:
            raise Exception(f"Could not set child {child_node_factory}") from e

    def get_source(self, node: Node, source: Any) -> Any:
        return source

    def make_node(self, factory: NodeFactory[Source, Target], source: Source) -> Optional[Node]:
        try:
            node = factory.constructor(source, self, factory)
            if node:
                node = node.with_origin(self.as_origin(source))
            return node
        except Exception as e:
            if self.allow_generic_node:
                return GenericErrorNode(error=e).with_origin(self.as_origin(source))
            else:
                raise e

    def get_node_factory(self, node_type: Type[Source]) -> Optional[NodeFactory[Source, Target]]:
        if node_type in self.factories:
            return self.factories[node_type]
        else:
            for superclass in node_type.__mro__:
                factory = self.get_node_factory(superclass)
                if factory:
                    return factory

    def register_node_factory(
            self, source: Type[Source], factory: Union[node_factory_constructor_type, Type[Target]]
    ) -> NodeFactory[Source, Target]:
        if isinstance(factory, type):
            node_factory = NodeFactory(lambda _, __, ___: factory())
        else:
            node_factory = NodeFactory(get_node_constructor_wrapper(factory))
        self.factories[source] = node_factory
        return node_factory

    def register_identity_transformation(self, node_class: Type[Target]):
        self.register_node_factory(node_class, lambda node: node)


def get_node_constructor_wrapper(decorated_function):
    try:
        sig = signature(decorated_function)
        try:
            sig.bind(1, 2, 3)
            wrapper = decorated_function
        except TypeError:
            try:
                sig.bind(1, 2)

                def wrapper(node: Node, parent: Node, _):
                    return decorated_function(node, parent)
            except TypeError:
                sig.bind(1)

                def wrapper(node: Node, _, __):
                    return decorated_function(node)
    except ValueError:
        wrapper = decorated_function

    functools.update_wrapper(wrapper, decorated_function)
    return wrapper


def ast_transformer(
        node_class: Type[Node],
        transformer: ASTTransformer,
        method_name: str = None):
    """Decorator to register a function as an AST transformer"""
    def decorator(decorated_function):
        if method_name:
            def transformer_method(self, parent: Optional[Node] = None):
                return transformer.transform(self, parent)
            setattr(node_class, method_name, transformer_method)
        if transformer:
            return transformer.register_node_factory(node_class, decorated_function).constructor
        else:
            return get_node_constructor_wrapper(decorated_function)

    return decorator
