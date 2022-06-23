from collections.abc import Iterable

from . import walk
from .model import Node, internal_property
from ..support import extension_method


@extension_method(Node)
def assign_parents(self: Node):
    """Sets or corrects the parent of all AST nodes.

    Pylasu does not see set/add/delete operations on the AST nodes, so this function should be called manually after
    modifying the AST, unless you've taken care of assigning the parents yourself.

    :param self: the root of the AST subtree to start from.
    """
    for node in children(self):
        node.parent = self
        assign_parents(node)


def children(self: Node):
    yield from nodes_in(v for _, v in self.properties)


Node.children = internal_property(children)


def nodes_in(iterable):
    for value in iterable:
        if isinstance(value, Node):
            yield value
        elif isinstance(value, Iterable) and not isinstance(value, str):
            yield from nodes_in(value)


@extension_method(Node)
def search_by_type(self: Node, target_type, walker=walk):
    for node in walker(self):
        if isinstance(node, target_type):
            yield node
