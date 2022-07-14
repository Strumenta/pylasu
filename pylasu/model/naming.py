from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, List


@dataclass
class PossiblyNamed:
    name: str = field(default=None)


@dataclass
class Named(PossiblyNamed):
    def __post_init__(self):
        if self.name is None:
            raise TypeError("missing 1 required positional argument: 'name'")


T = TypeVar("T", bound=PossiblyNamed)


@dataclass
class ReferenceByName(Generic[T]):
    name: str
    referred: Optional[T] = field(default=None)

    def __str__(self):
        status = 'Solved' if self.resolved() else 'Unsolved'
        return f"Ref({self.name})[{status}]"

    def __hash__(self):
        return self.name.__hash__() * (7 + 2 if self.resolved() else 1)

    def resolved(self):
        return self.referred is not None

    def try_to_resolve(self, candidates: List[T], case_insensitive: bool = False) -> bool:
        """
        Try to resolve the reference by finding a named element with a matching name.
        The name match is performed in a case sensitive or insensitive way depending on the value of caseInsensitive.
        """

        def check_name(candidate: T) -> bool:
            return candidate.name is not None and (
                candidate.name == self.name if not case_insensitive else candidate.name.lower() == self.name.lower())

        self.referred = next((candidate for candidate in candidates if check_name(candidate)), None)
        return self.resolved()
