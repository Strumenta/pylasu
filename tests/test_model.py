import dataclasses
import unittest

from pylasu.model import Node, Position, Point


@dataclasses.dataclass
class SomeNode(Node):
    foo = 3
    __private__ = 4

    def __post_init__(self):
        self.bar = 5


class ModelTest(unittest.TestCase):
    def test_empty_node(self):
        node = Node()
        self.assertIsNone(node.origin)

    def test_node_with_position(self):
        node = Node().with_position(Position(Point(1, 0), Point(2, 1)))
        self.assertEqual(Position(Point(1, 0), Point(2, 1)), node.position)
        node = SomeNode().with_position(Position(Point(1, 0), Point(2, 1)))
        self.assertEqual(Position(Point(1, 0), Point(2, 1)), node.position)

    def test_node_properties(self):
        node = SomeNode().with_position(Position(Point(1, 0), Point(2, 1)))
        self.assertIsNotNone(next(n for n, _ in node.properties if n == 'foo'))
        self.assertIsNotNone(next(n for n, _ in node.properties if n == 'bar'))
        with self.assertRaises(StopIteration):
            next(n for n, _ in node.properties if n == '__private__')
        with self.assertRaises(StopIteration):
            next(n for n, _ in node.properties if n == 'non_existent')
        with self.assertRaises(StopIteration):
            next(n for n, _ in node.properties if n == 'properties')
        with self.assertRaises(StopIteration):
            next(n for n, _ in node.properties if n == "origin")
