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

    def __add__(self, other):
        if isinstance(other, str):
            if len(other) == 0:
                return self
            line = self.line
            column = self.column
            i = 0
            while i < len(other):
                if other[i] == '\n' or other[i] == '\r':
                    line += 1
                    column = 0
                    if other[i] == '\r' and i < len(other) - 1 and other[i + 1] == '\n':
                        i += 1  # Count the \r\n sequence as 1 line
                else:
                    column += 1
                i += 1
            return Point(line, column)
        else:
            raise NotImplementedError()


@dataclass
class Position:
    start: Point
    end: Point

    def __post_init__(self):
        if self.end < self.start:
            raise Exception("End point can't be before starting point")


def pos(start_line: int, start_col: int, end_line: int, end_col: int):
    """Utility function to create a Position"""
    return Position(Point(start_line, start_col), Point(end_line, end_col))
