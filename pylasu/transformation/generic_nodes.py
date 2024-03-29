from dataclasses import dataclass

from pylasu.model import Node


@dataclass
class GenericNode(Node):
    """A generic AST node. We use it to represent parts of a source tree that we don't know how to translate yet."""
    parent: Node = None
