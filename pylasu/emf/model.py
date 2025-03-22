from enum import Enum

from deprecated import deprecated
from pyecore.ecore import EPackage
from pyecore.resources import Resource

from pylasu.model import Node
from pylasu.reflection.support import extension_method


@deprecated(reason="EMF Support is going to be dropped")
def find_eclassifier_in_resource(cls: type, resource: Resource):
    pkg_name = cls.__module__
    for p in resource.contents:
        if isinstance(p, EPackage) and p.name == pkg_name:
            return p.getEClassifier(cls.__name__)


@deprecated(reason="EMF Support is going to be dropped")
@extension_method(Resource)
def find_eclassifier(self: Resource, cls: type):
    eclass = find_eclassifier_in_resource(cls, self)
    if not eclass:
        for uri in self.resource_set.resources if self.resource_set else {}:
            resource = self.resource_set.resources[uri]
            if resource != self:
                eclass = find_eclassifier_in_resource(cls, resource)
                if eclass:
                    return eclass
    return eclass


@deprecated(reason="EMF Support is going to be dropped")
@extension_method(Node)
def to_eobject(self: Node, resource: Resource, mappings=None):
    if self is None:
        return None
    if mappings is None:
        mappings = {}
    elif id(self) in mappings:
        return mappings[id(self)]
    eclass = resource.find_eclassifier(type(self))
    if not eclass:
        raise Exception("Unknown classifier for " + str(type(self)))
    eobject = eclass()
    mappings[id(self)] = eobject
    for p in self.properties:
        v = p.value
        ev = translate_value(v, resource, mappings)
        if isinstance(v, list):
            eobject.eGet(p.name).extend(ev)
        else:
            eobject.eSet(p.name, ev)
    return eobject


@deprecated(reason="EMF Support is going to be dropped")
def translate_value(v, resource, mappings):
    if isinstance(v, Enum):
        enum_type = resource.find_eclassifier(type(v))
        if enum_type:
            return enum_type.getEEnumLiteral(v.name)
        else:
            raise Exception("Unknown enum " + str(type(v)))
    if isinstance(v, list):
        return [translate_value(x, resource, mappings) for x in v]
    elif isinstance(v, Node):
        return to_eobject(v, resource, mappings)
    else:
        return v
