from collections.abc import Iterable

from .model import Node, internal_property
from ..support import extension_method


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
def search_by_type(self: Node, target_type, walker=Node.walk):
    for node in walker(self):
        if isinstance(node, target_type):
            yield node
