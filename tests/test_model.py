import dataclasses
import unittest

from pylasu.model import Node, Position, Point
from pylasu.model.naming import ReferenceByName, Named


@dataclasses.dataclass
class SomeNode(Node, Named):
    foo = 3
    __private__ = 4

    def __post_init__(self):
        self.bar = 5


class ModelTest(unittest.TestCase):

    def test_reference_by_name_unsolved_str(self):
        ref_unsolved = ReferenceByName[SomeNode]("foo")
        self.assertEquals("Ref(foo)[Unsolved]", ref_unsolved.__str__())

    def test_reference_by_name_solved_str(self):
        ref_solved = ReferenceByName[SomeNode]("foo", SomeNode(name="foo"))
        self.assertEquals("Ref(foo)[Solved]", ref_solved.__str__())

    # try_to_resolve_positive_case_same_case
    def test_try_to_resolve_positive_case_same_case(self):
        ref = ReferenceByName[SomeNode]("foo")
        self.assertTrue(ref.try_to_resolve(candidates=[SomeNode(name="foo")]))

    # try_to_resolve_negative_case_same_case
    def test_try_to_resolve_negative_case_same_case(self):
        ref = ReferenceByName[SomeNode]("foo")
        self.assertFalse(ref.try_to_resolve(candidates=[SomeNode(name="not_foo")]))

    # try_to_resolve_positive_case_different_case
    def test_try_to_resolve_positive_case_different_case(self):
        ref = ReferenceByName[SomeNode]("foo")
        self.assertTrue(ref.try_to_resolve(candidates=[SomeNode(name="Foo")], case_insensitive=True))

    # try_to_resolve_negative_case_different_case
    def test_try_to_resolve_negative_case_different_case(self):
        ref = ReferenceByName[SomeNode]("foo")
        self.assertFalse(ref.try_to_resolve(candidates=[SomeNode(name="Foo")]))

    def test_empty_node(self):
        node = Node()
        self.assertIsNone(node.origin)

    def test_node_with_position(self):
        node = Node(position=Position(Point(1, 0), Point(2, 1)))
        self.assertEqual(Position(Point(1, 0), Point(2, 1)), node.position)
        node = SomeNode(position=Position(Point(1, 0), Point(2, 1)))
        self.assertEqual(Position(Point(1, 0), Point(2, 1)), node.position)

    def test_node_properties(self):
        node = SomeNode(position=Position(Point(1, 0), Point(2, 1)))
        self.assertIsNotNone(next(n for n, _ in node.properties if n == 'foo'))
        self.assertIsNotNone(next(n for n, _ in node.properties if n == 'bar'))
        self.assertIsNotNone(next(n for n, _ in node.properties if n == "name"))
        with self.assertRaises(StopIteration):
            next(n for n, _ in node.properties if n == '__private__')
        with self.assertRaises(StopIteration):
            next(n for n, _ in node.properties if n == 'non_existent')
        with self.assertRaises(StopIteration):
            next(n for n, _ in node.properties if n == 'properties')
        with self.assertRaises(StopIteration):
            next(n for n, _ in node.properties if n == "origin")
