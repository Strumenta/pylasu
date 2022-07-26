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

    def resolve(self, scope: 'Scope') -> bool:
        self.referred = scope.lookup(symbol_name=self.name)
        return self.resolved()

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


@dataclass
class Symbol(PossiblyNamed):
    pass


@dataclass
class Scope:
    # local symbols
    symbols: List[Symbol] = field(default_factory=list)
    # parent scope
    parent: Optional['Scope'] = field(default=None)

    # retrieve symbols from name, type or both
    def lookup(self, symbol_name: str = None, symbol_type: type = Symbol) -> List[Symbol]:
        # retrieve symbols from current scope
        local_symbols: List[Symbol] = self.__symbols(symbol_name, symbol_type)
        # retrieve symbols from upper scopes
        upper_symbols: List[Symbol] = self.parent.lookup(symbol_name, symbol_type) if self.parent else []
        # concatenate symbols with locals first
        return local_symbols + upper_symbols

    def __symbols(self, symbol_name: str = None, symbol_type: type = Symbol):
        def __check_symbol_name(symbol: Symbol) -> bool:
            # compare symbol name, ignore test if undefined (True)
            return symbol.name == symbol_name if symbol_name else True

        def __check_symbol_type(symbol: Symbol) -> bool:
            # compare symbol type, ignore test if undefined (True)
            return isinstance(symbol, symbol_type) if symbol_type else True

        # retrieve symbols from name, type or both
        return [symbol for symbol in self.symbols if
                __check_symbol_name(symbol) and __check_symbol_type(symbol)]
