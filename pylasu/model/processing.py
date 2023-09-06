from collections.abc import Iterable
from typing import Callable, List, Set

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
    yield from nodes_in(p.value for p in self.properties)


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


@extension_method(Node)
def transform_children(self: Node, operation: Callable[[Node], Node]):
    for prop in self.properties:
        name = prop.name
        value = prop.value
        if isinstance(value, Node):
            new_value = operation(value)
            if new_value != value:
                setattr(self, name, new_value)
        elif isinstance(value, List):
            setattr(self, name, [operation(item) if isinstance(item, Node) else item for item in value])
        elif isinstance(value, Set):
            raise Exception("Sets are not supported currently")


@extension_method(Node)
def replace_with(self: Node, other: Node):
    """Replace this node with another (by modifying the children of the parent node).
    For this to work, this node must have a parent assigned.

    :param self: the node to replace.
    :param other: the replacement node."""
    if not self.parent:
        raise Exception("Parent not set, cannot replace node")
    transform_children(self.parent, lambda x: other if x == self else x)
