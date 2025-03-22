from dataclasses import dataclass

from pylasu.lwmodel import ASTNode


@dataclass
class GenericNode(ASTNode):
    """A generic AST node. We use it to represent parts of a source tree that we don't know how to translate yet."""

    pass
