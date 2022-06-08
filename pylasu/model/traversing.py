from .model import Node
from ..support import extension_method


@extension_method(Node)
def walk(self: Node):
    yield self
    for child in self.children:
        yield from child.walk()


@extension_method(Node)
def walk_leaves_first(self: Node):
    for child in self.children:
        yield from child.walk_leaves_first()
    yield self
