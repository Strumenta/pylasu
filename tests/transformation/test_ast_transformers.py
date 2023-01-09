import enum
import unittest
from dataclasses import dataclass, field
from typing import List

from pylasu.model import Node
from pylasu.transformation.transformation import ASTTransformer, PropertyRef, ast_transformer


@dataclass
class CU(Node):
    statements: List[Node] = field(default_factory=list)


@dataclass
class DisplayIntStatement(Node):
    value: int = 0


@dataclass
class SetStatement(Node):
    variable: str = ""
    value: int = 0


class Operator(enum.Enum):
    PLUS = '+'
    MULT = '*'


class Expression(Node):
    pass


@dataclass
class IntLiteral(Expression):
    value: int


@dataclass
class GenericBinaryExpression(Node):
    operator: Operator
    left: Expression
    right: Expression


@dataclass
class Mult(Node):
    left: Expression
    right: Expression


@dataclass
class Sum(Node):
    left: Expression
    right: Expression


class ASTTransformerTest(unittest.TestCase):

    def test_identitiy_transformer(self):
        prop = PropertyRef("statements")
        transformer = ASTTransformer()
        transformer.register_node_factory(CU, CU).with_child(prop, prop)
        transformer.register_identity_transformation(DisplayIntStatement)
        transformer.register_identity_transformation(SetStatement)
        cu = CU(statements=[
                SetStatement(variable="foo", value=123),
                DisplayIntStatement(value=456)])
        transformed_cu = transformer.transform(cu)
        self.assertEqual(cu, transformed_cu)
        # assertTrue { transformed_cu.hasValidParents() }
        self.assertEquals(transformed_cu.origin, cu)

    def test_translate_binary_expression(self):
        """Example of transformation to perform a refactoring within the same language."""
        my_transformer = ASTTransformer(allow_generic_node=False)

        @ast_transformer(GenericBinaryExpression, my_transformer, "to_ast")
        def generic_binary_expression_to_ast(source: GenericBinaryExpression):
            if source.operator == Operator.MULT:
                return Mult(my_transformer.transform(source.left), my_transformer.transform(source.right))
            elif source.operator == Operator.PLUS:
                return Sum(my_transformer.transform(source.left), my_transformer.transform(source.right))

        my_transformer.register_identity_transformation(IntLiteral)
        source = GenericBinaryExpression(Operator.MULT, IntLiteral(7), IntLiteral(8))
        t1 = my_transformer.transform(source)
        self.assertEqual(t1, source.to_ast())

    def test_translate_across_languages(self):
        transformer = ASTTransformer(allow_generic_node=False)
        transformer.register_node_factory(ALangIntLiteral, lambda source: BLangIntLiteral(source.value))
        transformer.register_node_factory(
            ALangSum,
            lambda source: BLangSum(transformer.transform(source.left), transformer.transform(source.right)))
        transformer.register_node_factory(
            ALangMult,
            lambda source: BLangMult(transformer.transform(source.left), transformer.transform(source.right)))
        self.assertEqual(
            BLangMult(
                BLangSum(
                    BLangIntLiteral(1),
                    BLangMult(BLangIntLiteral(2), BLangIntLiteral(3))
                ),
                BLangIntLiteral(4)
            ),
            transformer.transform(
                ALangMult(
                    ALangSum(
                        ALangIntLiteral(1),
                        ALangMult(ALangIntLiteral(2), ALangIntLiteral(3))
                    ),
                    ALangIntLiteral(4))))


@dataclass
class ALangExpression(Node):
    pass


@dataclass
class ALangIntLiteral(ALangExpression):
    value: int


@dataclass
class ALangSum(ALangExpression):
    left: ALangExpression
    right: ALangExpression



@dataclass
class ALangMult(ALangExpression):
    left: ALangExpression
    right: ALangExpression


@dataclass
class BLangExpression(Node):
    pass


@dataclass
class BLangIntLiteral(BLangExpression):
    value: int


@dataclass
class BLangSum(BLangExpression):
    left: BLangExpression
    right: BLangExpression



@dataclass
class BLangMult(BLangExpression):
    left: BLangExpression
    right: BLangExpression


if __name__ == '__main__':
    unittest.main()
