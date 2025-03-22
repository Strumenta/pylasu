from dataclasses import dataclass, field
from typing import List

from pylasu.model import Node, internal_field, pos


@dataclass
class Box(Node):
    name: str = None
    contents: List[Node] = field(default_factory=list)
    internal: str = internal_field(default="unused")


@dataclass
class Item(Node):
    name: str = None


@dataclass
class ReinforcedBox(Box):
    strength: int = 10


box = Box(
    name="root",
    contents=[
        Box("first", [Item("1").with_position(pos(3, 6, 3, 12))]).with_position(pos(2, 3, 4, 3)),
        Item(name="2").with_position(pos(5, 3, 5, 9)),
        Box(
            name="big",
            contents=[
                Box(
                    name="small",
                    contents=[
                        Item(name="3").with_position(pos(8, 7, 8, 13)),
                        Item(name="4").with_position(pos(9, 7, 9, 13)),
                        Item(name="5").with_position(pos(10, 7, 10, 13))
                    ]
                ).with_position(pos(7, 5, 11, 5))
            ]
        ).with_position(pos(6, 3, 12, 3)),
        Item(name="6").with_position(pos(13, 3, 13, 9))
    ]
).with_position(pos(1, 1, 14, 1))
