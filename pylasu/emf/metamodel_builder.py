import typing
from collections.abc import Callable
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


def get_type_origin(tp):
    if hasattr(typing, "get_origin"):
        return typing.get_origin(tp)
    elif hasattr(tp, "__origin__"):
        return tp.__origin__
    elif tp is typing.Generic:
        return typing.Generic
    else:
        return None


def is_enum_type(attr_type):
    return isinstance(attr_type, EnumMeta) and issubclass(attr_type, Enum)


def is_sequence_type(attr_type):
    return isinstance(get_type_origin(attr_type), type) and \
           issubclass(get_type_origin(attr_type), typing.Sequence)


def get_type_arguments(tp):
    if hasattr(typing, "get_args"):
        return typing.get_args(tp)
    elif hasattr(tp, "__args__"):
        res = tp.__args__
        if get_type_origin(tp) is Callable and res[0] is not Ellipsis:
            res = (list(res[:-1]), res[-1])
        return res
    return ()


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
            nmspc = self.setup_attributes(cls)
            bases = self.setup_base_classes(cls)
            eclass = MetaEClass(cls.__name__, resolve_bases(tuple(bases)), nmspc)
            eclass.eClass.ePackage = self.package
            for (type_name, ref) in self.forward_references:
                if type_name == cls.__name__:
                    ref.eType = eclass
            self.forward_references = [(t, r) for t, r in self.forward_references if not r.eType]
        return eclass

    def setup_base_classes(self, cls):
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
        return bases

    def setup_attributes(self, cls):
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
        return nmspc

    def to_structural_feature(self, attr, attr_type, unsupported_type_handler=None):  # noqa: C901
        def raise_on_unsupported_type(attr_type, attr):
            raise Exception("Unsupported type " + str(attr_type) + " for attribute " + attr)

        def default_unsupported_type(_, __):
            return EObject

        if not unsupported_type_handler:
            unsupported_type_handler = raise_on_unsupported_type
        if isinstance(attr_type, str):
            return self.to_reference(attr, attr_type)
        elif attr_type in self.data_types:
            return EAttribute(attr, self.data_types[attr_type])
        elif attr_type == object:
            return EAttribute(attr)
        elif self.is_node_type(attr_type):
            return EReference(attr, self.provide_class(attr_type), containment=True)
        elif is_sequence_type(attr_type):
            return self.to_list_reference(attr, attr_type, default_unsupported_type)
        elif get_type_origin(attr_type) == typing.Union:
            return EReference(attr, EObject, containment=True)  # TODO here we could refine the type better
        elif is_enum_type(attr_type):
            return self.to_enum_attribute(attr, attr_type)
        else:
            return unsupported_type_handler(attr_type, attr)

    def is_node_type(self, attr_type):
        return isinstance(attr_type, type) and issubclass(attr_type, self.base_node_class)

    def to_enum_attribute(self, attr, attr_type):
        tp = EEnum(name=attr_type.__name__, literals=attr_type.__members__)
        tp.ePackage = self.package
        self.data_types[attr_type] = tp
        return EAttribute(attr, tp)

    def to_list_reference(self, attr, attr_type, default_unsupported_type):
        type_args = get_type_arguments(attr_type)
        if type_args and len(type_args) == 1:
            ft = self.to_structural_feature(attr, type_args[0], default_unsupported_type)
            ft.upperBound = -1
            return ft
        else:
            raise "Unsupported list type: " + str(attr_type)

    def to_reference(self, attr, attr_type):
        resolved = self.package.getEClassifier(attr_type)
        if resolved:
            return EReference(attr, resolved, containment=True)
        else:
            forward_reference = EReference(attr, containment=True)
            self.forward_references.append((attr_type, forward_reference))
            return forward_reference

    def generate(self):
        if self.forward_references:
            raise Exception("The following classes are missing from " + self.package.name + ": "
                            + ", ".join(n for n, _ in self.forward_references))
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
