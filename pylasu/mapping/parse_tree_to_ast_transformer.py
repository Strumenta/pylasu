from typing import Any, Optional

from antlr4 import ParserRuleContext
from antlr4.tree.Tree import ParseTree

from pylasu.model import Node, Origin
from pylasu.parsing.parse_tree import ParseTreeOrigin, with_parse_tree
from pylasu.transformation.transformation import ASTTransformer


class ParseTreeToASTTransformer(ASTTransformer):
    """Implements a transformation from an ANTLR parse tree (the output of the parser) to an AST
    (a higher-level representation of the source code)."""

    def transform(
        self, source: Optional[Any], parent: Optional[Node] = None
    ) -> Optional[Node]:
        """Performs the transformation of a node and, recursively, its descendants. In addition to the overridden
        method, it also assigns the parseTreeNode to the AST node so that it can keep track of its position.
        However, a node factory can override the parseTreeNode of the nodes it creates (but not the parent).
        """
        node = super().transform(source, parent)
        if node and node.origin and isinstance(source, ParserRuleContext):
            with_parse_tree(node, source)
        return node

    def get_source(self, node: Node, source: Any) -> Any:
        origin = node.origin
        if isinstance(origin, ParseTreeOrigin):
            return origin.parse_tree
        else:
            return source

    def as_origin(self, source: Any) -> Optional[Origin]:
        if isinstance(source, ParseTree):
            return ParseTreeOrigin(source)
        else:
            return None
