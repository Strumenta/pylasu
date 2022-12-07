from dataclasses import dataclass
from typing import Any, Dict, Callable, TypeVar, Generic, Optional, List, Set, Iterable

from pylasu.model import Node
from pylasu.validation import Issue

Child = TypeVar('Child')
Output = TypeVar('Output', bound=Node)
Source = TypeVar('Source')
Target = TypeVar('Target')


@dataclass
class NodeFactory(Generic[Source, Output]):
    constructor: Callable[[Source, "ASTTransformer", "NodeFactory[Source, Output]"], Optional[Output]]
    children: Dict[str, "ChildNodeFactory[Source, Any, Any]"]
    finalizer: Callable[[Source], None]

    def with_child(
            self,
            getter: Callable[[Source], Optional[Any]],
            setter: Callable[[Target, Optional[Child]], None],
            name: str,
            target_type: Optional[type] = None
    ) -> "NodeFactory[Source, Output]":
        if target_type:
            prefix = target_type.__qualname__ + "#"
        else:
            prefix = ""
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
            raise Exception("Mapping error: received collection when value was expected")
        node = None
        factory = self.get_node_factory(type(source))
        if factory:
            node = self.make_node(factory, source)
            if not node:
                return None
            node.properties
        # TODO
