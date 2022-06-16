from dataclasses import dataclass, field
from typing import List

from pylasu.model import Node, pos


@dataclass
class Box(Node):
    name: str = None
    contents: List[Node] = field(default_factory=list)


@dataclass
class Item(Node):
    name: str = None


box = Box(
    name="root",
    contents=[
        Box(name="first", contents=[Item(name="1", position=pos(3, 6, 3, 12))],
            position=pos(2, 3, 4, 3)),
        Item(name="2", position=pos(5, 3, 5, 9)),
        Box(
            name="big",
            contents=[
                Box(
                    name="small",
                    contents=[
                        Item(name="3", position=pos(8, 7, 8, 13)),
                        Item(name="4", position=pos(9, 7, 9, 13)),
                        Item(name="5", position=pos(10, 7, 10, 13))
                    ],
                    position=pos(7, 5, 11, 5)
                )
            ],
            position=pos(6, 3, 12, 3)
        ),
        Item(name="6", position=pos(13, 3, 13, 9))
    ],
    position=pos(1, 1, 14, 1)
)
