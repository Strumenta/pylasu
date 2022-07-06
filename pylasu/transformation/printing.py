from dataclasses import dataclass
from typing import Sequence

from pylasu.model import Node
from pylasu.model.model import internal_property


@dataclass
class NodeWithSyntax(Node):
    syntax_before: str = ""
    syntax_after: str = ""

    @internal_property
    def syntax_before(self) -> str:
        return self._syntax_before

    @syntax_before.setter
    def syntax_before(self, syntax: str):
        self._syntax_before = syntax

    @internal_property
    def syntax_after(self) -> str:
        return self._syntax_after

    @syntax_after.setter
    def syntax_after(self, syntax: str):
        self._syntax_after = syntax

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
