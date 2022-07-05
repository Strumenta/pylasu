from dataclasses import dataclass
from typing import Sequence

from pylasu.model import Node


@dataclass
class NodeWithSyntax(Node):
    syntax_before: str = ""
    syntax_after: str = ""

    def as_syntax(self):
        for _, child in self.properties:
            if isinstance(child, Sequence):
                for x in child:
                    yield x
            elif child is not None:
                yield child

    def to_string(self):
        result = ""
        result += self.syntax_before if self.syntax_before else ""
        for node in self.as_syntax():
            if isinstance(node, str):
                result += node
            elif isinstance(node, NodeWithSyntax):
                result += node.to_string()
            else:
                result += str(node)
        result += self.syntax_after if self.syntax_after else ""
        return result
