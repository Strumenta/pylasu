import unittest

import pylasu.StrumentaLanguageSupport as starlasu_metamodel
from pylasu.StrumentaLanguageSupport import ASTNode
from pylasu.playground.transpilation_trace import TranspilationTrace
from pyecore.ecore import EString, EAttribute, EInt


class ANode(ASTNode):
    name = EAttribute(eType=EString)
    value = EAttribute(eType=EInt)

    def __init__(self, *, name=None, value=None, **kwargs):
        super().__init__(**kwargs)
        if name is not None:
            self.name = name
        if value is not None:
            self.value = value


class ModelTest(unittest.TestCase):

    def test_serialize_transpilation_issue(self):
        tt = TranspilationTrace(
            original_code="a:1", generated_code="b:2",
            source_result=starlasu_metamodel.Result(root=ANode(name="a", value=1)),
            target_result=starlasu_metamodel.Result(root=ANode(name="b", value=2)),
            issues=[starlasu_metamodel.Issue(
                type=starlasu_metamodel.IssueType.getEEnumLiteral("TRANSLATION"),
                message="some issue",
                severity=starlasu_metamodel.IssueSeverity.getEEnumLiteral("WARNING"))]
        )
        self.assertEqual("a:1", tt.original_code)
        self.assertEqual("b:2", tt.generated_code)
        self.assertEqual("some issue", tt.issues[0].message)
        self.assertEqual("a", tt.source_result.root.name)
        self.assertEqual(1, tt.source_result.root.value)
        self.assertEqual("b", tt.target_result.root.name)
        self.assertEqual(2, tt.target_result.root.value)
