import unittest
from dataclasses import dataclass, field
from typing import List

from pylasu.model import Node
from pylasu.transformation.transformation import ASTTransformer, node_property


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


class ASTTransformerTest(unittest.TestCase):

    def test_identitiy_transformer(self):
        prop = node_property("statements", CU)
        transformer = ASTTransformer()
        transformer.register_node_factory(CU, CU).with_child(prop[0], prop[1], "statements")
        transformer.register_identity_transformation(DisplayIntStatement)
        transformer.register_identity_transformation(SetStatement)
        cu = CU(statements=[
                SetStatement(variable="foo", value=123),
                DisplayIntStatement(value=456)])
        transformed_cu = transformer.transform(cu)
        # assertASTsAreEqual(cu, transformed_cu, considerPosition = true)
        # assertTrue { transformed_cu.hasValidParents() }
        self.assertEquals(transformed_cu.origin, cu)


if __name__ == '__main__':
    unittest.main()
