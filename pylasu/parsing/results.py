from dataclasses import dataclass, field
from typing import List

from antlr4 import ParserRuleContext, Token

from pylasu.model import Source
from pylasu.validation.validation import WithIssues, IssueType, Issue


@dataclass
class FirstStageResult(WithIssues):
    parse_tree: ParserRuleContext
    issues: List[Issue] = field(default_factory=list)


@dataclass
class LexingResult(WithIssues):
    tokens: List[Token]
    issues: List[Issue] = field(default_factory=list)


@dataclass
class IssuesErrorListener:
    """This Error Listener should be used with ANTLR lexers and parsers to capture issues"""
    type: IssueType
    source: Source
    issues: WithIssues

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.issues.append(Issue(type=self.type, message=msg))

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        pass

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        pass

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        pass
