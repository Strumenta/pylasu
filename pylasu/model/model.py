from abc import ABC, abstractmethod
from dataclasses import dataclass, field, InitVar
import inspect

from .position import Position


class Origin(ABC):
    @property
    @abstractmethod
    def position(self) -> Position or None:
        pass

    @property
    def source_text(self) -> str or None:
        return None


@dataclass
class JustPosition(Origin):
    position: Position
    _position: Position = field(init=False, repr=False)

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, position: Position):
        self._position = position


@dataclass
class Node(Origin):
    origin: Origin = None
    specified_position: InitVar[Position] = None

    def __post_init__(self, specified_position: Position):
        if specified_position is not None:
            if self.origin is not None:
                raise Exception("Cannot provide an explicit position when the origin is also specified")
            else:
                self.origin = JustPosition(specified_position)

    @property
    def position(self) -> Position:
        return self.origin.position

    @position.setter
    def position(self, position: Position):
        if self.origin is None or isinstance(self.origin, JustPosition):
            self.origin = JustPosition(position)
        else:
            raise Exception("Origin already set, cannot change position")

    @property
    def source_text(self) -> str or None:
        return self.origin.source_text

    @property
    def properties(self):
        return (name for name in dir(self) if not name.startswith('__') and name != 'properties')
