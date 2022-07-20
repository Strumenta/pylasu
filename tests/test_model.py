import dataclasses
import unittest

from pylasu.model import Node, Position, Point
from pylasu.model.naming import ReferenceByName, Named, Scope, Symbol


@dataclasses.dataclass
class SomeNode(Node, Named):
    foo = 3
    __private__ = 4

    def __post_init__(self):
        self.bar = 5


class ModelTest(unittest.TestCase):

    def test_reference_by_name_unsolved_str(self):
        ref_unsolved = ReferenceByName[SomeNode]("foo")
        self.assertEqual("Ref(foo)[Unsolved]", str(ref_unsolved))

    def test_reference_by_name_solved_str(self):
        ref_solved = ReferenceByName[SomeNode]("foo", SomeNode(name="foo"))
        self.assertEqual("Ref(foo)[Solved]", str(ref_solved))

    def test_scope_lookup_symbol_in_empty_scope(self):
        scope: Scope = Scope()
        self.assertIsNone(scope.lookup("foo"))

    def test_try_to_resolve_positive_case_same_case(self):
        ref = ReferenceByName[SomeNode]("foo")
        self.assertTrue(ref.try_to_resolve(candidates=[SomeNode(name="foo")]))

    def test_try_to_resolve_negative_case_same_case(self):
        ref = ReferenceByName[SomeNode]("foo")
        self.assertFalse(ref.try_to_resolve(candidates=[SomeNode(name="not_foo")]))

    def test_try_to_resolve_positive_case_different_case(self):
        ref = ReferenceByName[SomeNode]("foo")
        self.assertTrue(ref.try_to_resolve(candidates=[SomeNode(name="Foo")], case_insensitive=True))

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

    def test_scope_lookup_symbol_in_current_scope(self):
        symbol: Symbol = Symbol(name="foo")
        scope: Scope = Scope(symbols={"foo": symbol}, parent=None)
        self.assertEquals(symbol, scope.lookup("foo"))

    def test_scope_lookup_symbol_in_current_scope_with_shadowing(self):
        symbol: Symbol = Symbol(name="foo")
        shadow: Symbol = Symbol(name="foo")
        scope: Scope = Scope(symbols={"foo": symbol}, parent=Scope(symbols={"foo": shadow}, parent=None))
        self.assertEquals(symbol, scope.lookup("foo"))

    def test_scope_lookup_symbol_in_parent_scope(self):
        symbol: Symbol = Symbol(name="foo")
        scope: Scope = Scope(symbols={}, parent=Scope(symbols={"foo": symbol}, parent=None))
        self.assertEquals(symbol, scope.lookup("foo"))

    def test_scope_lookup_symbol_in_parent_scope_with_shadowing(self):
        symbol: Symbol = Symbol(name="foo")
        shadow: Symbol = Symbol(name="foo")
        scope: Scope = Scope(symbols={},
                             parent=Scope(symbols={"foo": symbol}, parent=Scope(symbols={"foo": shadow}, parent=None)))
        self.assertEquals(symbol, scope.lookup("foo"))
