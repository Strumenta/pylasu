from . import Position
from .model import Node
from ..support import extension_method


@extension_method(Node)
def walk(self: Node):
    """Walks the whole AST starting from this node, depth-first."""
    yield self
    for child in self.children:
        yield from walk(child)


@extension_method(Node)
def walk_within(self: Node, position: Position):
    """Walks the AST within the given [position] starting from this node, depth-first.
    :param self: the node from which to start the walk.
    :param position: the position within which the walk should remain."""
    if self.position in position:
        yield self
        for child in self.children:
            yield from walk_within(child, position)
    elif position in self.position:
        for child in self.children:
            yield from walk_within(child, position)


@extension_method(Node)
def walk_leaves_first(self: Node):
    """Performs a post-order (or leaves-first) node traversal starting with a given node."""
    for child in self.children:
        yield from walk_leaves_first(child)
    yield self


@extension_method(Node)
def walk_ancestors(self: Node):
    """Iterator over the sequence of nodes from this node's parent all the way up to the root node."""
    if self.parent is not None:
        yield self.parent
        yield from walk_ancestors(self.parent)


@extension_method(Node)
def walk_descendants(self: Node, walker=walk, restrict_to=Node):
    """Walks the whole AST starting from the child nodes of this node.

    :param self: the node from which to start the walk, which is NOT included in the walk.
    :param walker: a function that generates a sequence of nodes. By default this is the depth-first "walk" method.
    For post-order traversal, use "walk_leaves_first".
    :param restrict_to: optional type filter. By default, all nodes (i.e., subclasses of Node) are included, but you can
    limit the walk to only a subtype of Node.
    """
    for node in walker(self):
        if node != self and isinstance(node, restrict_to):
            yield node


@extension_method(Node)
def find_ancestor_of_type(self: Node, target: type):
    """Returns the nearest ancestor of this node that is an instance of the target type.

    Note that type is not strictly forced to be a subtype of Node. This is intended to support trait types like
    `Statement` or `Expression`. However, the returned value is guaranteed to be a Node, as only Node instances can be
    part of the hierarchy.

    :param self: the node from which to start the search.
    :param target: the target type.
    """
    for node in walk_ancestors(self):
        if isinstance(node, target):
            return node
