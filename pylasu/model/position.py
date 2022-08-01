from dataclasses import dataclass
from pathlib import Path


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

    def __repr__(self):
        return f"Line {self.line}, Column {self.column}"

    def __str__(self):
        return f"{self.line}:{self.column}"


class Source:
    pass


@dataclass
class SourceSet:
    name: str
    root: Path


@dataclass
class SourceSetElement(Source):
    sourceSet: SourceSet
    relativePath: Path


@dataclass
class FileSource(Source):
    file: Path

    def __str__(self):
        return str(self.file)


@dataclass
class StringSource(Source):
    code: str = None


@dataclass
class URLSource(Source):
    url: str = None


@dataclass
class Position:
    """An area in a source file, from start to end.
    The start point is the point right before the starting character.
    The end point is the point right after the last character.
    An empty position will have coinciding points.

    Consider a file with one line, containing the text "HELLO".
    The Position of such text will be Position(Point(1, 0), Point(1, 5))."""
    start: Point
    end: Point
    source: Source = None

    def __post_init__(self):
        if self.end < self.start:
            raise Exception("End point can't be before starting point")

    def __contains__(self, pos):
        return isinstance(pos, Position) and self.start <= pos.start and self.end >= pos.end

    def __repr__(self):
        return f"Position(start={self.start}, end={self.end}"\
               + (f", source={self.source}" if self.source is not None else "")

    def __str__(self):
        str_rep = (f"{self.source}:" if self.source is not None else "") + str(self.start)
        if self.start != self.end:
            str_rep += f"-{self.end}"
        return str_rep


def pos(start_line: int, start_col: int, end_line: int, end_col: int, source: Source = None):
    """Utility function to create a Position"""
    return Position(Point(start_line, start_col), Point(end_line, end_col), source)
