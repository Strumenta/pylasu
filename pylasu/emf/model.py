from pyecore.ecore import EPackage
from pyecore.resources import Resource

from pylasu.model import Node
from pylasu.support import extension_method


def find_eclass_in_resource(cls: type, resource: Resource):
    pkg_name = cls.__module__
    for p in resource.contents:
        if isinstance(p, EPackage) and p.name == pkg_name:
            return p.getEClassifier(cls.__name__)


@extension_method(Resource)
def find_eclass(self: Resource, cls: type):
    eclass = find_eclass_in_resource(cls, self)
    if not eclass:
        for uri in (self.resource_set.resources if self.resource_set else {}):
            resource = self.resource_set.resources[uri]
            if resource != self:
                eclass = find_eclass_in_resource(cls, resource)
                if eclass:
                    return eclass
    return eclass


@extension_method(Node)
def to_eobject(self: Node, resource: Resource, mappings=None):
    if mappings is None:
        mappings = {}
    eclass = resource.find_eclass(type(self))
    if not eclass:
        raise Exception("Unknown eclass for " + str(type(self)))
    eobject = eclass()
    return eobject
