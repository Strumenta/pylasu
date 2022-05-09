import unittest

from pylasu.model import Node, Position, Point


class ModelTest(unittest.TestCase):
    def test_node_with_position(self):
        node = Node(specified_position=Position(Point(1, 0), Point(2, 1)))
        self.assertIsNotNone(node.origin)
        self.assertEqual(Position(Point(1, 0), Point(2, 1)), node.position)
