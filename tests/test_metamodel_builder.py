import unittest
from pyecore.ecore import EObject

from pylasu.emf.metamodel_builder import MetamodelBuilder
from tests.fixtures import Box, ReinforcedBox


class MetamodelBuilderTest(unittest.TestCase):
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
