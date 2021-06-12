from dataclasses import dataclass


@dataclass
class Named:
    name: str


@dataclass
class Point:
    line: int
    column: int


@dataclass
class Position:
    start: Point
    end: Point


@dataclass
class ASTNode:
    position: Position


@dataclass
class ReferenceByName:
    name: str
