from typing import Sequence

from pylasu.model import Node
from pylasu.model.model import internal_properties


@internal_properties("syntax_before", "syntax_after")
class NodeWithSyntax(Node):
    syntax_before: str = ""
    syntax_after: str = ""

    def __post_init__(self):
        if isinstance(self.syntax_before, property):
            self.syntax_before = ""
        if isinstance(self.syntax_after, property):
            self.syntax_after = ""

    def as_syntax(self):
        for _, child in self.properties:
            if isinstance(child, Sequence) and not isinstance(child, str):
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
