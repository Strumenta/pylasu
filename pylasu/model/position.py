from dataclasses import dataclass


@dataclass
class Point:
    line: int
    column: int

    def __post_init__(self):
        if self.line < 1:
            raise Exception(f"Line {self.line} cannot be less than 1")
        if self.column < 0:
            raise Exception(f"Column {self.column} cannot be less than 0")

    def __lt__(self, other):
        if isinstance(other, Point):
            return self.line < other.line or (self.line == other.line and self.column < other.column)
        else:
            raise NotImplementedError()

    def __le__(self, other):
        if isinstance(other, Point):
            return self.line < other.line or (self.line == other.line and self.column <= other.column)
        else:
            raise NotImplementedError()


@dataclass
class Position:
    start: Point
    end: Point

    def __post_init__(self):
        if self.end < self.start:
            raise Exception("End point can't be before starting point")
