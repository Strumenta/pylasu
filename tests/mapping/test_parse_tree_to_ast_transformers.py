import unittest
from dataclasses import dataclass, field
from typing import List

from antlr4 import CommonTokenStream, InputStream

from pylasu.mapping.parse_tree_to_ast_transformer import ParseTreeToASTTransformer
from pylasu.model import Node, Named, ReferenceByName
from pylasu.transformation.transformation import PropertyRef
from tests.antlr_entity.AntlrEntityLexer import AntlrEntityLexer
from tests.antlr_entity.AntlrEntityParser import AntlrEntityParser


@dataclass
class EModule(Node, Named):
    entities: List["EEntity"] = field(default_factory=list)


@dataclass
class EEntity(Node, Named):
    features: List["EFeature"] = field(default_factory=list)


@dataclass
class EFeature(Node, Named):
    type: "EType" = None


class EType(Node):
    pass


@dataclass
class EBooleanType(EType):
    pass


@dataclass
class EStringType(EType):
    pass


@dataclass
class EEntityRefType(EType):
    entity: ReferenceByName[EEntity]


class ParseTreeToASTTransformerTest(unittest.TestCase):

    def test_simple_entities_transformer(self):
        transformer = ParseTreeToASTTransformer(allow_generic_node=False)
        transformer.register_node_factory(AntlrEntityParser.ModuleContext, lambda ctx: EModule(name=ctx.name.text)) \
            .with_child(PropertyRef("entities"), AntlrEntityParser.ModuleContext.entity)
        transformer.register_node_factory(AntlrEntityParser.EntityContext, lambda ctx: EEntity(name=ctx.name.text))
        expected_ast = EModule("M", [EEntity("FOO", []), EEntity("BAR", [])])
        actual_ast = transformer.transform(self.parse_entities("""
module M {
   entity FOO { }
   entity BAR { }
}
        """))
        self.assertEqual(expected_ast, actual_ast)

    def test_entities_with_features_transformer(self):
        transformer = ParseTreeToASTTransformer(allow_generic_node=False)
        transformer.register_node_factory(AntlrEntityParser.ModuleContext, lambda ctx: EModule(name=ctx.name.text)) \
            .with_child(PropertyRef("entities"), AntlrEntityParser.ModuleContext.entity)
        transformer.register_node_factory(AntlrEntityParser.EntityContext, lambda ctx: EEntity(name=ctx.name.text)) \
            .with_child(PropertyRef("features"), AntlrEntityParser.EntityContext.feature)
        transformer.register_node_factory(AntlrEntityParser.FeatureContext, lambda ctx: EFeature(name=ctx.name.text)) \
            .with_child(PropertyRef("type"), AntlrEntityParser.FeatureContext.type_spec)
        transformer.register_node_factory(AntlrEntityParser.Boolean_typeContext, EBooleanType)
        transformer.register_node_factory(AntlrEntityParser.String_typeContext, EStringType)
        transformer.register_node_factory(
            AntlrEntityParser.Entity_typeContext,
            lambda ctx: EEntityRefType(ReferenceByName(ctx.target.text)))

        expected_ast = EModule(
            "M",
            [
                EEntity(
                    "FOO",
                    [EFeature("A", EStringType()), EFeature("B", EBooleanType())]
                ),
                EEntity(
                    "BAR",
                    [EFeature("C", EEntityRefType(ReferenceByName("FOO")))]
                )
            ]
        )
        actual_ast = transformer.transform(
            self.parse_entities("""
            module M {
              entity FOO {
                A: string;
                B: boolean;
              }
              entity BAR {
                C: FOO;
              }
            }"""))
        self.assertEqual(expected_ast, actual_ast)

    def parse_entities(self, code: str) -> AntlrEntityParser.ModuleContext:
        lexer = AntlrEntityLexer(InputStream(code))
        parser = AntlrEntityParser(CommonTokenStream(lexer))
        return parser.module()


if __name__ == '__main__':
    unittest.main()
