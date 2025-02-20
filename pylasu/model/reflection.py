import enum
from dataclasses import dataclass
from typing import Optional


class Multiplicity(enum.Enum):
    OPTIONAL = 0
    SINGULAR = 1
    MANY = 2


@dataclass
class PropertyDescription:
    name: str
    type: Optional[type]
    is_containment: bool
    is_reference: bool
    multiplicity: Multiplicity = Multiplicity.SINGULAR
    value: object = None

    @property
    def multiple(self):
        return self.multiplicity == Multiplicity.MANY
