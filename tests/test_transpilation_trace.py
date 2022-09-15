import json
import unittest

from pyecore.ecore import EString, EAttribute, EInt

import pylasu.StrumentaLanguageSupport as starlasu
from pylasu.StrumentaLanguageSupport import ASTNode
from pylasu.emf import MetamodelBuilder
from pylasu.playground import TranspilationTrace, ETranspilationTrace
from pylasu.validation.validation import Result
from tests.fixtures import Box, Item

nsURI = "http://mypackage.com"
name = "StrumentaLanguageSupportTranspilationTest"


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
        tt = ETranspilationTrace(
            original_code="a:1", generated_code="b:2",
            source_result=starlasu.Result(root=ANode(name="a", value=1)),
            target_result=starlasu.Result(root=ANode(name="b", value=2)),
            issues=[starlasu.Issue(
                type=starlasu.IssueType.getEEnumLiteral("TRANSLATION"),
                message="some issue",
                severity=starlasu.IssueSeverity.getEEnumLiteral("WARNING"))]
        )
        self.assertEqual("a:1", tt.originalCode)
        self.assertEqual("b:2", tt.generatedCode)
        self.assertEqual("some issue", tt.issues[0].message)
        self.assertEqual("a", tt.sourceResult.root.name)
        self.assertEqual(1, tt.sourceResult.root.value)
        self.assertEqual("b", tt.targetResult.root.name)
        self.assertEqual(2, tt.targetResult.root.value)

        expected = """{
  "eClass" : "https://strumenta.com/kolasu/transpilation/v1#//TranspilationTrace",
  "originalCode" : "a:1",
  "sourceResult" : {
    "root" : {
      "eClass" : "http://mypackage.com#//ANode",
      "name" : "a",
      "value" : 1
    }
  },
  "targetResult" : {
    "root" : {
      "eClass" : "http://mypackage.com#//ANode",
      "name" : "b",
      "value" : 2
    }
  },
  "generatedCode" : "b:2",
  "issues" : [ {
    "message" : "some issue",
    "severity" : "WARNING"
  } ]
}"""
        self.assertEqual(json.loads(expected), json.loads(tt.save_as_json("foo.json")))

    def test_serialize_transpilation_from_nodes(self):
        mmb = MetamodelBuilder("tests.fixtures", "https://strumenta.com/pylasu/test/fixtures")
        mmb.provide_class(Box)
        mmb.provide_class(Item)

        tt = TranspilationTrace(
            original_code="box(a)[i1, bar]", generated_code='<box name="A"><i1 /><bar /></box>',
            source_result=Result(Box("a", [Item("i1"), Box("b", [Item("i2"), Item("i3")])])),
            target_result=Result(Box("A")))

        expected = """{
            "eClass": "https://strumenta.com/kolasu/transpilation/v1#//TranspilationTrace",
            "generatedCode": "<box name=\\"A\\"><i1 /><bar /></box>",
            "originalCode": "box(a)[i1, bar]",
            "sourceResult": { "root": {
                "eClass": "https://strumenta.com/pylasu/test/fixtures#//Box",
                "name": "a",
                "contents": [{
                    "eClass": "https://strumenta.com/pylasu/test/fixtures#//Item",
                    "name": "i1"
                    }, {
                        "eClass": "https://strumenta.com/pylasu/test/fixtures#//Box",
                        "name": "b",
                        "contents": [{
                            "eClass": "https://strumenta.com/pylasu/test/fixtures#//Item",
                            "name": "i2"
                        }, {
                            "eClass": "https://strumenta.com/pylasu/test/fixtures#//Item",
                            "name": "i3"
                        }]
                    }]
                }
            },
            "targetResult": { "root": {
                "eClass": "https://strumenta.com/pylasu/test/fixtures#//Box", 
                "name": "A",
                "contents": []
                }
            }
        }"""
        as_json = tt.save_as_json("foo.json", mmb.generate())
        self.assertEqual(json.loads(expected), json.loads(as_json))
