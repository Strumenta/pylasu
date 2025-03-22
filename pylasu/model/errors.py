from dataclasses import dataclass
from typing import Optional

from pylasu.model import Node, Position


@dataclass
class ErrorNode:
    """An AST node that marks the presence of an error,
    for example a syntactic or semantic error in the original tree."""

    message: str = None
    position: Optional[Position] = None


@dataclass
class GenericErrorNode(Node, ErrorNode):
    error: Optional[Exception] = None

    def __post_init__(self):
        if not self.message:
            if self.error:
                self.message = f"Exception {self.error}"
            else:
                self.message = "Unspecified error node"
