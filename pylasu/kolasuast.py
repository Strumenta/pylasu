from dataclasses import dataclass


@dataclass
class Named:
    name: str


@dataclass
class ReferenceByName:
    name: str
