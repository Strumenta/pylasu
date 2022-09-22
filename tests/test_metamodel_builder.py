import json
import unittest
from io import BytesIO, IOBase

from pyecore.ecore import EObject, EPackage, EEnum, EMetaclass, EAttribute, EString
from pyecore.resources import URI

from pylasu.StrumentaLanguageSupport import ASTNode
from pylasu.emf import MetamodelBuilder
from pylasu.playground import JsonResource
from tests.fixtures import Box, ReinforcedBox


eClass = EPackage('test', nsURI='http://test/1.0', nsPrefix='test')
nsURI = 'http://test/1.0'
nsPrefix = 'test'

BookCategory = EEnum('BookCategory', literals=['ScienceFiction', 'Biographie', 'Mistery'])
eClass.eClassifiers.append(BookCategory)


@EMetaclass
class A(object):
    names = EAttribute(eType=EString, upper=-1)
    bcat = EAttribute(eType=BookCategory)


class MetamodelBuilderTest(unittest.TestCase):
    def test_pyecore_enum(self):
        from pyecore.resources import ResourceSet
        from pyecore.resources.json import JsonResource as BaseJsonResource

        class TestJsonResource(BaseJsonResource):
            def open_out_stream(self, other=None):
                if isinstance(other, IOBase):
                    return other
                else:
                    return super().open_out_stream(other)

        rset = ResourceSet()
        rset.resource_factory['json'] = lambda uri: TestJsonResource(uri=uri, indent=2)
        resource = rset.create_resource('ZMM.json')
        resource.append(eClass)
        with BytesIO() as out:
            resource.save(out)
            self.assertEqual(json.loads(out.getvalue().decode("utf-8")), json.loads('''{
  "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EPackage",
  "nsPrefix": "test",
  "nsURI": "http://test/1.0",
  "name": "test",
  "eClassifiers": [
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EEnum",
      "name": "BookCategory",
      "eLiterals": [
        "ScienceFiction",
        "Biographie",
        "Mistery"
      ]
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "eStructuralFeatures": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "upperBound": -1,
          "name": "names",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EDataType",
            "$ref": "#//EString"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "bcat",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EEnum",
            "$ref": "#//BookCategory"
          }
        }
      ],
      "name": "A"
    }
  ]
}'''))

    def test_can_serialize_starlasu_model(self):
        starlasu_package = ASTNode.eClass.ePackage
        resource = JsonResource(URI(starlasu_package.nsURI))
        resource.contents.append(starlasu_package)
        with BytesIO() as out:
            resource.save(out)
            starlasu_model = json.loads(STARLASU_MODEL_JSON)
            serialized_model = json.loads(out.getvalue().decode('utf-8'))
            self.maxDiff = None
            self.assertDictEqual(serialized_model, starlasu_model)

    def test_build_metamodel_single_package(self):
        mb = MetamodelBuilder("tests.fixtures", "https://strumenta.com/pylasu/test/fixtures")
        box = mb.provide_class(Box)
        self.assertIsInstance(box(), EObject)
        self.assertEqual(box.eClass.ePackage, mb.package)
        self.assertTrue(box.eClass in mb.package.eContents)
        self.assertIsNotNone(
            next((a for a in box.eClass.eAllAttributes() if a.name == "name"), None))
        self.assertEqual(1, len(box.eClass.eAllAttributes()))

    def test_build_metamodel_single_package_inheritance(self):
        mb = MetamodelBuilder("tests.fixtures", "https://strumenta.com/pylasu/test/fixtures")
        box = mb.provide_class(ReinforcedBox)
        self.assertIsInstance(box(), EObject)
        self.assertEqual(box.eClass.ePackage, mb.package)
        self.assertEqual(2, len(mb.package.eContents))
        self.assertTrue(box.eClass in mb.package.eContents)
        self.assertIsNotNone(
            next((a for a in box.eClass.eAllAttributes() if a.name == "name"), None))
        self.assertIsNotNone(
            next((a for a in box.eClass.eAllAttributes() if a.name == "strength"), None))
        self.assertEqual(2, len(box.eClass.eAllAttributes()))


STARLASU_MODEL_JSON = '''{
  "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EPackage",
  "eClassifiers": [
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "eStructuralFeatures": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "year",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EDataType",
            "$ref": "#//EInt"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "month",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EDataType",
            "$ref": "#//EInt"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "dayOfMonth",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EDataType",
            "$ref": "#//EInt"
          }
        }
      ],
      "name": "LocalDate"
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "eStructuralFeatures": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "hour",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EDataType",
            "$ref": "#//EInt"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "minute",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EDataType",
            "$ref": "#//EInt"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "second",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EDataType",
            "$ref": "#//EInt"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "nanosecond",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EDataType",
            "$ref": "#//EInt"
          }
        }
      ],
      "name": "LocalTime"
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "eStructuralFeatures": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EReference",
          "containment": true,
          "name": "date",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
            "$ref": "#//LocalDate"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EReference",
          "containment": true,
          "name": "time",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
            "$ref": "#//LocalTime"
          }
        }
      ],
      "name": "LocalDateTime"
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "eStructuralFeatures": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "line",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EDataType",
            "$ref": "#//EInt"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "column",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EDataType",
            "$ref": "#//EInt"
          }
        }
      ],
      "name": "Point"
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "eStructuralFeatures": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EReference",
          "containment": true,
          "name": "start",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
            "$ref": "#//Point"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EReference",
          "containment": true,
          "name": "end",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
            "$ref": "#//Point"
          }
        }
      ],
      "name": "Position"
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "name": "Origin",
      "abstract": true
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "name": "Destination",
      "abstract": true
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "name": "Statement"
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "name": "Expression"
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "name": "EntityDeclaration"
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "eStructuralFeatures": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "type",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EEnum",
            "$ref": "#//IssueType"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "message",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EDataType",
            "$ref": "#//EString"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "severity",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EEnum",
            "$ref": "#//IssueSeverity"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EReference",
          "containment": true,
          "name": "position",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
            "$ref": "#//Position"
          }
        }
      ],
      "name": "Issue"
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "eStructuralFeatures": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "name",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EDataType",
            "$ref": "#//EString"
          }
        }
      ],
      "name": "PossiblyNamed"
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "eStructuralFeatures": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "name",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EDataType",
            "$ref": "#//EString"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EReference",
          "name": "referenced",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
            "$ref": "#//ASTNode"
          }
        }
      ],
      "name": "ReferenceByName"
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "eStructuralFeatures": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EReference",
          "containment": true,
          "name": "root",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
            "$ref": "#//ASTNode"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EReference",
          "upperBound": -1,
          "containment": true,
          "name": "issues",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
            "$ref": "#//Issue"
          }
        }
      ],
      "name": "Result"
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "eStructuralFeatures": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EReference",
          "name": "node",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
            "$ref": "#//ASTNode"
          }
        }
      ],
      "eSuperTypes": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
          "$ref": "#//Destination"
        }
      ],
      "name": "NodeDestination"
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "eStructuralFeatures": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EReference",
          "containment": true,
          "name": "position",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
            "$ref": "#//Position"
          }
        }
      ],
      "eSuperTypes": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
          "$ref": "#//Destination"
        }
      ],
      "name": "TextFileDestination"
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "eStructuralFeatures": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EReference",
          "containment": true,
          "name": "position",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
            "$ref": "#//Position"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EReference",
          "name": "origin",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
            "$ref": "#//Origin"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EReference",
          "containment": true,
          "name": "destination",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
            "$ref": "#//Destination"
          }
        }
      ],
      "eSuperTypes": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
          "$ref": "#//Origin"
        }
      ],
      "name": "ASTNode",
      "abstract": true
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "eStructuralFeatures": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "name",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EDataType",
            "$ref": "#//EString"
          }
        }
      ],
      "eSuperTypes": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
          "$ref": "#//PossiblyNamed"
        }
      ],
      "name": "Named"
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EDataType",
      "instanceClassName": "java.math.BigDecimal",
      "name": "BigDecimal"
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EDataType",
      "instanceClassName": "java.math.BigInteger",
      "name": "BigInteger"
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EEnum",
      "eLiterals": [
        "LEXICAL",
        "SYNTACTIC",
        "SEMANTIC"
      ],
      "name": "IssueType"
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EEnum",
      "eLiterals": [
        "ERROR",
        "WARNING",
        "INFO"
      ],
      "name": "IssueSeverity"
    }
  ],
  "name": "StrumentaLanguageSupport",
  "nsURI": "https://strumenta.com/kolasu/v2",
  "nsPrefix": ""
}'''
