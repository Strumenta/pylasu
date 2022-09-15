from pyecore.ecore import EAttribute, EObject, EPackage, EReference, MetaEClass, EString, EInt
from pyecore.resources import Resource

from pylasu import StrumentaLanguageSupport as starlasu
from pylasu.StrumentaLanguageSupport import ASTNode
from pylasu.model import Node


class MetamodelBuilder:
    def __init__(self, package_name: str, ns_uri: str, ns_prefix: str = None, resource: Resource = None):
        self.package = EPackage(package_name, ns_uri, ns_prefix)
        if resource:
            resource.append(self.package)

    def can_provide_class(self, cls: type):
        return cls.__module__ == self.package.name

    def provide_class(self, cls: type):
        if not self.can_provide_class(cls):
            raise Exception(self.package.name + " cannot provide class " + str(cls))
        eclass = self.package.getEClassifier(cls.__name__)
        if not eclass:
            anns = getannotations(cls)
            nmspc = {
                "position": EReference("position", starlasu.Position, containment=True)
            }
            for attr in anns:
                if anns[attr] == str:
                    nmspc[attr] = EAttribute(attr, EString)
                elif anns[attr] == int:
                    nmspc[attr] = EAttribute(attr, EInt)
            bases = []
            for c in cls.__mro__[1:]:
                if c == Node:
                    bases.append(ASTNode)
                elif self.can_provide_class(c):
                    bases.append(self.provide_class(c))
            bases.append(EObject)
            eclass = MetaEClass(cls.__name__, tuple(bases), nmspc)
            eclass.eClass.ePackage = self.package
        return eclass

    def generate(self):
        return self.package


def getannotations(cls):
    import inspect
    try:  # On Python 3.10+
        return inspect.getannotations(cls)
    except AttributeError:
        if isinstance(cls, type):
            return cls.__dict__.get('__annotations__', None)
        else:
            return getattr(cls, '__annotations__', None)
