import unittest
from dataclasses import dataclass, field
from typing import List

from antlr4 import CommonTokenStream, InputStream

from pylasu.mapping.parse_tree_to_ast_transformer import ParseTreeToASTTransformer
from pylasu.model import Node, Named
from pylasu.transformation.transformation import PropertyRef
from tests.antlr_entity.AntlrEntityLexer import AntlrEntityLexer
from tests.antlr_entity.AntlrEntityParser import AntlrEntityParser


@dataclass
class EModule(Node, Named):
    entities: List["EEntity"] = field(default_factory=list)


@dataclass
class EEntity(Node, Named):
    features: List = field(default_factory=list)


class ParseTreeToASTTransformerTest(unittest.TestCase):

    def test_simple_entities_transformer(self):
        transformer = ParseTreeToASTTransformer(allow_generic_node=False)
        transformer.register_node_factory(
            AntlrEntityParser.ModuleContext, lambda ctx: EModule(name=ctx.name.text))\
            .with_child(AntlrEntityParser.ModuleContext.entity, PropertyRef("entities"))
        transformer.register_node_factory(AntlrEntityParser.EntityContext, lambda ctx: EEntity(name=ctx.name.text))
        expected_ast = EModule("M", [EEntity("FOO", []), EEntity("BAR", [])])
        actual_ast = transformer.transform(self.parse_entities("""
module M {
   entity FOO { }
   entity BAR { }
}
        """))
        self.assertEqual(expected_ast, actual_ast)

    def parse_entities(self, code: str) -> AntlrEntityParser.ModuleContext:
        lexer = AntlrEntityLexer(InputStream(code))
        parser = AntlrEntityParser(CommonTokenStream(lexer))
        return parser.module()


if __name__ == '__main__':
    unittest.main()
