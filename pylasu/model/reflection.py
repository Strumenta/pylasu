import enum
from dataclasses import dataclass


class Multiplicity(enum.Enum):
    OPTIONAL = 0
    SINGULAR = 1
    MANY = 2


@dataclass
class PropertyDescription:
    name: str
    provides_nodes: bool
    multiplicity: Multiplicity = Multiplicity.SINGULAR
    value: object = None

    @property
    def multiple(self):
        return self.multiplicity == Multiplicity.MANY
