from dataclasses import dataclass, field
from typing import Any, Dict, Callable, TypeVar, Generic, Optional

from pylasu.model import Node

Child = TypeVar('Child')
Output = TypeVar('Output', bound=Node)
Source = TypeVar('Source')
Target = TypeVar('Target')


@dataclass
class NodeFactory(Generic[Source, Output]):
    constructor: Callable[[Source, "ASTTransformer", "NodeFactory[Source, Output]"], Optional[Output]]
    children: Dict[str, "ChildNodeFactory[Source, Any, Any]"]
    finalizer: Callable[[Source], None]


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


class ASTTransformer:
    pass
