from abc import ABC


class Expression(ABC):
    pass


class PlaceholderElement(ABC):
    pass


class TypeAnnotation(ABC):
    pass


class Parameter(ABC):
    pass


class Statement(ABC):
    pass


class EntityDeclaration(ABC):
    pass


class BehaviorDeclaration(ABC):
    pass


class Documentation(ABC):
    pass


class Named(ABC):

    @property
    def name(self) -> str:
        pass
