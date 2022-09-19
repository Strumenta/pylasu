import typing
from dataclasses import is_dataclass, fields
from enum import Enum, EnumMeta
from types import resolve_bases

from pyecore.ecore import EAttribute, ECollection, EObject, EPackage, EReference, MetaEClass, EBoolean, EString, EInt, \
    EEnum
from pyecore.resources import Resource
from pylasu import StrumentaLanguageSupport as starlasu
from pylasu.StrumentaLanguageSupport import ASTNode
from pylasu.emf.model import find_eclassifier
from pylasu.model import Node
from pylasu.model.model import InternalField


class MetamodelBuilder:
    def __init__(self, package_name: str, ns_uri: str, ns_prefix: str = None, resource: Resource = None,
                 base_node_class: type = Node):
        self.package = EPackage(package_name, ns_uri, ns_prefix)
        if resource:
            resource.append(self.package)
        self.data_types = {
            bool: EBoolean,
            int: EInt,
            str: EString,
        }
        self.base_node_class = base_node_class
        self.forward_references = []

    def can_provide_class(self, cls: type):
        return cls.__module__ == self.package.name

    def provide_class(self, cls: type):
        if cls == self.base_node_class:
            return ASTNode
        if not self.can_provide_class(cls):
            if self.package.eResource:
                eclass = find_eclassifier(self.package.eResource, cls)
                if eclass:
                    return eclass
            raise Exception(self.package.name + " cannot provide class " + str(cls))
        eclass = self.package.getEClassifier(cls.__name__)
        if not eclass:
            anns = getannotations(cls)
            nmspc = {
                "position": EReference("position", starlasu.Position, containment=True)
            }
            for attr in anns if anns else []:
                if attr.startswith('_'):
                    continue
                elif is_dataclass(cls):
                    field = next((f for f in fields(cls) if f.name == attr), None)
                    if isinstance(field, InternalField):
                        continue
                attr_type = anns[attr]
                nmspc[attr] = self.to_structural_feature(attr, attr_type)
            bases = []
            for c in cls.__mro__[1:]:
                if c == self.base_node_class:
                    bases.append(ASTNode)
                elif self.can_provide_class(c):
                    bases.append(self.provide_class(c))
                elif self.package.eResource:
                    esuperclass = find_eclassifier(self.package.eResource, c)
                    if esuperclass:
                        bases.append(esuperclass)
            bases.append(EObject)
            eclass = MetaEClass(cls.__name__, resolve_bases(tuple(bases)), nmspc)
            eclass.eClass.ePackage = self.package
            for (type_name, ref) in self.forward_references:
                if type_name == cls.__name__:
                    ref.eType = eclass
            self.forward_references = [(t, r) for t, r in self.forward_references if not r.eType]
        return eclass

    def to_structural_feature(self, attr, attr_type, unsupported_type_handler=None):
        def raise_on_unsupported_type(attr_type, attr):
            raise Exception("Unsupported type " + str(attr_type) + " for attribute " + attr)

        def default_unsupported_type(_, __):
            return EObject

        if not unsupported_type_handler:
            unsupported_type_handler = raise_on_unsupported_type
        if isinstance(attr_type, str):
            resolved = self.package.getEClassifier(attr_type)
            if resolved:
                return EReference(attr, resolved, containment=True)
            else:
                forward_reference = EReference(attr, containment=True)
                self.forward_references.append((attr_type, forward_reference))
                return forward_reference
        elif attr_type in self.data_types:
            return EAttribute(attr, self.data_types[attr_type])
        elif attr_type == object:
            return EAttribute(attr)
        elif isinstance(attr_type, type) and issubclass(attr_type, self.base_node_class):
            return EReference(attr, self.provide_class(attr_type), containment=True)
        elif isinstance(typing.get_origin(attr_type), type) and \
                issubclass(typing.get_origin(attr_type), typing.Sequence):
            type_args = typing.get_args(attr_type)
            if type_args and len(type_args) == 1:
                ft = self.to_structural_feature(attr, type_args[0], default_unsupported_type)
                ft.upperBound = -1
                return ft
        elif typing.get_origin(attr_type) == typing.Union:
            return EReference(attr, EObject, containment=True)  # TODO here we could refine the type better
        elif isinstance(attr_type, EnumMeta) and issubclass(attr_type, Enum):
            tp = EEnum(name=attr_type.__name__, literals=attr_type.__members__)
            tp.ePackage = self.package
            self.data_types[attr_type] = tp
            return EAttribute(attr, tp)
        else:
            return unsupported_type_handler(attr_type, attr)

    def generate(self):
        if self.forward_references:
            raise Exception("The following classes are missing from " + self.package.name + ": " +
                            ", ".join(n for n, _ in self.forward_references))
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


# Monkey patch until fix
update_opposite = ECollection._update_opposite


def update_opposite_if_not_none(self, owner, new_value, remove=False):
    if owner:
        update_opposite(self, owner, new_value, remove)


ECollection._update_opposite = update_opposite_if_not_none
