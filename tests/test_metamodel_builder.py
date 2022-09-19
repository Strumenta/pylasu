import json
import unittest
from io import BytesIO

from pyecore.ecore import EObject
from pyecore.resources import URI

from pylasu.StrumentaLanguageSupport import ASTNode
from pylasu.emf import MetamodelBuilder
from pylasu.playground import JsonResource
from tests.fixtures import Box, ReinforcedBox


class MetamodelBuilderTest(unittest.TestCase):
    def test_can_serialize_starlasu_model(self):
        starlasu_package = ASTNode.eClass.ePackage
        resource = JsonResource(URI(starlasu_package.nsURI))
        resource.contents.append(starlasu_package)
        with BytesIO() as out:
            resource.save(out)
            self.assertEqual(json.loads(out.getvalue().decode('utf-8')), json.loads(STARLASU_MODEL_JSON))

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
            "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
            "$ref": "#//EInt"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "month",
          "eType": {
            "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
            "$ref": "#//EInt"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "dayOfMonth",
          "eType": {
            "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
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
            "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
            "$ref": "#//EInt"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "minute",
          "eType": {
            "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
            "$ref": "#//EInt"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "second",
          "eType": {
            "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
            "$ref": "#//EInt"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "nanosecond",
          "eType": {
            "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
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
            "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
            "$ref": "#//EInt"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "column",
          "eType": {
            "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
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
            "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
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
            "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
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
            "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
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
            "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
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
      "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
      "instanceClassName": "java.math.BigDecimal",
      "name": "BigDecimal"
    },
    {
      "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
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
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "eStructuralFeatures": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "instanceClassName",
          "eType": {
            "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
            "$ref": "#//EString"
          }
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EAttribute",
          "name": "serializable",
          "eType": {
            "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
            "$ref": "#//EBoolean"
          }
        }
      ],
      "eSuperTypes": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
          "$ref": "#//EClassifier"
        }
      ],
      "eOperations": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EOperation",
          "eParameters": [
            {
              "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EParameter",
              "name": "self",
              "required": true,
              "eType": {
                "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
                "$ref": "#//ENativeType"
              }
            },
            {
              "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EParameter",
              "name": "value",
              "required": true,
              "eType": {
                "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
                "$ref": "#//ENativeType"
              }
            }
          ],
          "name": "from_string"
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EOperation",
          "eParameters": [
            {
              "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EParameter",
              "name": "self",
              "required": true,
              "eType": {
                "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
                "$ref": "#//ENativeType"
              }
            },
            {
              "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EParameter",
              "name": "value",
              "required": true,
              "eType": {
                "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
                "$ref": "#//ENativeType"
              }
            }
          ],
          "name": "to_string"
        }
      ],
      "name": "EDataType"
    },
    {
      "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
      "eStructuralFeatures": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EReference",
          "upperBound": -1,
          "containment": true,
          "name": "eLiterals",
          "eType": {
            "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
            "$ref": "#//EEnumLiteral"
          }
        }
      ],
      "eSuperTypes": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EClass",
          "$ref": "#//EDataType"
        }
      ],
      "eOperations": [
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EOperation",
          "eParameters": [
            {
              "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EParameter",
              "name": "self",
              "required": true,
              "eType": {
                "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
                "$ref": "#//ENativeType"
              }
            },
            {
              "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EParameter",
              "name": "notif",
              "required": true,
              "eType": {
                "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
                "$ref": "#//ENativeType"
              }
            }
          ],
          "name": "notifyChanged"
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EOperation",
          "eParameters": [
            {
              "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EParameter",
              "name": "self",
              "required": true,
              "eType": {
                "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
                "$ref": "#//ENativeType"
              }
            },
            {
              "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EParameter",
              "name": "name",
              "eType": {
                "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
                "$ref": "#//ENativeType"
              }
            },
            {
              "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EParameter",
              "name": "value",
              "eType": {
                "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
                "$ref": "#//ENativeType"
              }
            }
          ],
          "name": "getEEnumLiteral"
        },
        {
          "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EOperation",
          "eParameters": [
            {
              "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EParameter",
              "name": "self",
              "required": true,
              "eType": {
                "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
                "$ref": "#//ENativeType"
              }
            },
            {
              "eClass": "http://www.eclipse.org/emf/2002/Ecore#//EParameter",
              "name": "value",
              "required": true,
              "eType": {
                "eClass": "https://strumenta.com/kolasu/v2#//EDataType",
                "$ref": "#//ENativeType"
              }
            }
          ],
          "name": "from_string"
        }
      ],
      "name": "EEnum"
    }
  ],
  "name": "StrumentaLanguageSupport",
  "nsURI": "https://strumenta.com/kolasu/v2",
  "nsPrefix": ""
}'''
