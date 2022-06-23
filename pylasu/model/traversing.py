from . import Position
from .model import Node
from ..support import extension_method


@extension_method(Node)
def walk(self: Node):
    """Walks the whole AST starting from this node, depth-first."""
    yield self
    for child in self.children:
        yield from child.walk()


@extension_method(Node)
def walk_leaves_first(self: Node):
    """Performs a post-order (or leaves-first) node traversal starting with a given node."""
    for child in self.children:
        yield from child.walk_leaves_first()
    yield self


@extension_method(Node)
def walk_within(self: Node, position: Position):
    """Walks the AST within the given [position] starting from this node, depth-first.
    :param self: the node from which to start the walk.
    :param position: the position within which the walk should remain."""
    if self.position in position:
        yield self
        for child in self.children:
            yield from child.walk_within(position)
    elif position in self.position:
        for child in self.children:
            yield from child.walk_within(position)
