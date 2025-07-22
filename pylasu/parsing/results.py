from dataclasses import dataclass, field
from typing import List, Optional

from pylasu.model import Source, Node
from pylasu.validation.validation import Issue


@dataclass
class FirstStageParsingResult:
    issues: List[Issue]
    root: Optional[Node]
    code: Optional[str] = None
    time: int = None
    lexing_time: int = None
    source: Source = None


@dataclass
class ParsingResultWithFirstStage:
    issues: List[Issue] = field(default_factory=list)
    root: Node = None
    code: str = None
    time: int = None
    first_stage: FirstStageParsingResult = None
    source: Source = None
