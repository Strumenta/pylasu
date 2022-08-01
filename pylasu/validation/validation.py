import enum
from dataclasses import dataclass
from typing import List

from pylasu.model import Position, Node


class IssueType(enum.Enum):
    LEXICAL = 0
    SYNTACTIC = 1
    SEMANTIC = 2


class IssueSeverity(enum.Enum):
    ERROR = 30
    WARNING = 20
    INFO = 10


@dataclass
class Issue:
    type: IssueType
    message: str
    severity: IssueSeverity = IssueSeverity.ERROR
    position: Position = None

    def __str__(self):
        msg = f"{self.severity.name.capitalize()} ({self.type.name.lower()}): {self.message}"
        if self.position:
            msg += f" @ {self.position}"
        return msg


@dataclass
class Result:
    root: Node
    issues: List[Issue]
