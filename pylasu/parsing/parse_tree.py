from dataclasses import dataclass
from antlr4 import ParserRuleContext, TerminalNode, Token
from antlr4.tree.Tree import ParseTree

from pylasu.model import Origin, Position, Point
from pylasu.support import extension_method


@dataclass
class ParseTreeOrigin(Origin):
    parse_tree: ParseTree

    @property
    def position(self) -> Position or None:
        return self.parse_tree.to_position()


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
def to_position(self: ParserRuleContext):
    return Position(self.start.start_point, self.stop.end_point)


@extension_method(TerminalNode)
def to_position(self: TerminalNode):  # noqa: F811
    return Position(self.symbol.start_point, self.symbol.end_point)
    # We ignore F811 (redefinition of unused function) because this is an extension method and needs to be called
    # to_position. It's not an actual redefinition.
