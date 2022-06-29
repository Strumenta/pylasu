from dataclasses import dataclass
from typing import Optional

from antlr4 import ParserRuleContext, TerminalNode, Token
from antlr4.tree.Tree import ParseTree

from pylasu.model import Origin, Position, Point
from pylasu.model.position import Source
from pylasu.support import extension_method


@dataclass
class ParseTreeOrigin(Origin):
    parse_tree: ParseTree
    source: Source = None

    @property
    def position(self) -> Optional[Position]:
        return self.parse_tree.to_position(self.source)


def token_start_point(token: Token):
    return Point(token.line, token.column)


def token_end_point(token: Token):
    if token.type == Token.EOF:
        return token.start_point
    else:
        return token.start_point + token.text


Token.start_point = property(token_start_point)
Token.end_point = property(token_end_point)


@extension_method(ParserRuleContext)
def to_position(self: ParserRuleContext, source: Source = None):
    return Position(self.start.start_point, self.stop.end_point, source)


@extension_method(TerminalNode)
def to_position(self: TerminalNode, source: Source = None):
    return self.symbol.to_position(source)


@extension_method(Token)
def to_position(self: Token, source: Source = None):
    return Position(self.start_point, self.end_point, source)
