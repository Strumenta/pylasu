from dataclasses import dataclass, field
from itertools import chain
from typing import Dict, Generic, List, Optional, TypeVar


@dataclass
class PossiblyNamed:
    name: Optional[str]

    def __init__(self, name: Optional[str] = None):
        self.name = name


@dataclass
class Named(PossiblyNamed):
    name: str


T = TypeVar("T", bound=PossiblyNamed)


@dataclass
class ReferenceByName(Generic[T]):
    name: str
    referred: Optional[T] = field(default=None)

    def __str__(self):
        status = "Solved" if self.resolved() else "Unsolved"
        return f"Ref({self.name})[{status}]"

    def __hash__(self):
        return self.name.__hash__() * (7 + 2 if self.resolved() else 1)

    def resolved(self):
        return self.referred is not None

    def resolve(self, scope: "Scope", case_insensitive: bool = False) -> bool:
        self.referred = scope.lookup(
            symbol_name=self.name, case_insensitive=case_insensitive
        )
        return self.resolved()

    def try_to_resolve(
        self, candidates: List[T], case_insensitive: bool = False
    ) -> bool:
        """
        Try to resolve the reference by finding a named element with a matching name.
        The name match is performed in a case sensitive or insensitive way depending on the value of case_insensitive.
        """

        def check_name(candidate: T) -> bool:
            return candidate.name is not None and (
                candidate.name == self.name
                if not case_insensitive
                else candidate.name.lower() == self.name.lower()
            )

        self.referred = next(
            (candidate for candidate in candidates if check_name(candidate)), None
        )
        return self.resolved()


@dataclass
class Symbol(PossiblyNamed):
    pass


@dataclass
class Scope:
    symbols: Dict[str, List[Symbol]] = field(default_factory=list)
    parent: Optional["Scope"] = field(default=None)
    insensitive_map: Optional[Dict[str, List[str]]] = field(default=None)

    def lookup(
        self,
        symbol_name: str,
        symbol_type: type = Symbol,
        case_insensitive: bool = False,
    ) -> Optional[Symbol]:
        if case_insensitive:
            if self.insensitive_map is None:
                self.insensitive_map = {}
                for key in self.symbols.keys():
                    key_lower: str = key.lower()
                    self.insensitive_map[key_lower] = self.insensitive_map.get(
                        key_lower, []
                    ) + [key]

            symbol_name_lower: str = symbol_name.lower()

            return next(
                (
                    symbol
                    for symbol in chain.from_iterable(
                        self.symbols.get(orig_symbol_name, [])
                        for orig_symbol_name in self.insensitive_map[symbol_name_lower]
                    )
                    if isinstance(symbol, symbol_type)
                ),
                (
                    self.parent.lookup(symbol_name, symbol_type)
                    if self.parent is not None
                    else None
                ),
            )

        return next(
            (
                symbol
                for symbol in self.symbols.get(symbol_name, [])
                if isinstance(symbol, symbol_type)
            ),
            (
                self.parent.lookup(symbol_name, symbol_type)
                if self.parent is not None
                else None
            ),
        )

    def add(self, symbol: Symbol):
        self.symbols[symbol.name] = self.symbols.get(symbol.name, []) + [symbol]

        if self.insensitive_map is not None:
            symbol_name_lower: str = symbol.name.lower()
            self.insensitive_map[symbol_name_lower] = self.insensitive_map.get(
                symbol_name_lower, []
            ) + [symbol.name]
