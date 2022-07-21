import dataclasses
import unittest

from pylasu.model import Node, Position, Point
from pylasu.model.naming import ReferenceByName, Named, Scope, Symbol
from typing import List


@dataclasses.dataclass
class SomeNode(Node, Named):
    foo = 3
    __private__ = 4

    def __post_init__(self):
        self.bar = 5


@dataclasses.dataclass
class SomeSymbol(Symbol):
    index: int = dataclasses.field(default=None)


@dataclasses.dataclass
class AnotherSymbol(Symbol):
    index: int = dataclasses.field(default=None)


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

    def test_scope_lookup_symbol_by_name_found(self):
        local_symbol_0 = SomeSymbol(name="a", index=0)
        local_symbol_1 = SomeSymbol(name="a", index=1)
        upper_symbol_0 = SomeSymbol(name="b", index=2)
        upper_symbol_1 = SomeSymbol(name="a", index=3)
        root_symbol_0 = SomeSymbol(name="a", index=4)
        root_symbol_1 = SomeSymbol(name="b", index=5)
        scope = Scope(symbols=[local_symbol_0, local_symbol_1],
                      parent=Scope(symbols=[upper_symbol_0, upper_symbol_1],
                                   parent=Scope(symbols=[root_symbol_0, root_symbol_1],
                                                parent=None)))
        # retrieve all symbols with name 'a'
        result = scope.lookup("a")
        self.assertEquals(len(result), 4)
        self.assertEquals(result[0], local_symbol_0)
        self.assertEquals(result[1], local_symbol_1)
        self.assertEquals(result[2], upper_symbol_1)
        self.assertEquals(result[3], root_symbol_0)

    def test_scope_lookup_symbol_by_name_not_found(self):
        local_symbol = SomeSymbol(name="a", index=0)
        upper_symbol = SomeSymbol(name="b", index=1)
        root_symbol = SomeSymbol(name="c", index=2)
        scope = Scope(symbols=[local_symbol],
                      parent=Scope(symbols=[upper_symbol],
                                   parent=Scope(symbols=[root_symbol],
                                                parent=None)))
        # retrieve all symbols with name 'd'
        result = scope.lookup("d")
        self.assertEquals(len(result), 0)

    def test_scope_lookup_symbol_by_type_found(self):
        local_symbol_0 = Symbol(name="a")
        local_symbol_1 = SomeSymbol(name="b", index=0)
        upper_symbol_0 = SomeSymbol(name="a", index=1)
        upper_symbol_1 = Symbol(name="a")
        root_symbol_0 = Symbol(name="a")
        root_symbol_1 = SomeSymbol(name="b", index=2)
        scope = Scope(symbols=[local_symbol_0, local_symbol_1],
                      parent=Scope(symbols=[upper_symbol_0, upper_symbol_1],
                                   parent=Scope(symbols=[root_symbol_0, root_symbol_1],
                                                parent=None)))
        # retrieve all symbols of type SomeSymbol
        result = scope.lookup(symbol_type=SomeSymbol)
        self.assertEquals(len(result), 3)
        self.assertEquals(result[0], local_symbol_1)
        self.assertEquals(result[1], upper_symbol_0)
        self.assertEquals(result[2], root_symbol_1)
        # retrieve all symbols of type Symbol
        result = scope.lookup(symbol_type=Symbol)
        self.assertEquals(len(result), 6)
        self.assertEquals(result[0], local_symbol_0)
        self.assertEquals(result[1], local_symbol_1)
        self.assertEquals(result[2], upper_symbol_0)
        self.assertEquals(result[3], upper_symbol_1)
        self.assertEquals(result[4], root_symbol_0)
        self.assertEquals(result[5], root_symbol_1)

    def test_scope_lookup_symbol_by_type_not_found(self):
        local_symbol = Symbol(name="a")
        upper_symbol = Symbol(name="b")
        root_symbol = Symbol(name="c")
        scope = Scope(symbols=[local_symbol],
                      parent=Scope(symbols=[upper_symbol],
                                   parent=Scope(symbols=[root_symbol],
                                                parent=None)))
        # retrieve all symbols of type SomeSymbol
        result = scope.lookup(symbol_type=SomeSymbol)
        self.assertEquals(len(result), 0)

        # retrieve all symbols of type Symbol
        result = scope.lookup(symbol_type=Symbol)
        self.assertEquals(len(result), 3)
        self.assertEquals(result[0], local_symbol)
        self.assertEquals(result[1], upper_symbol)
        self.assertEquals(result[2], root_symbol)

    def test_scope_lookup_symbol_by_name_and_type_found(self):
        local_symbol_0 = Symbol(name="a")
        local_symbol_1 = SomeSymbol(name="b", index=0)
        upper_symbol_0 = SomeSymbol(name="a", index=1)
        upper_symbol_1 = Symbol(name="b")
        root_symbol_0 = Symbol(name="a")
        root_symbol_1 = SomeSymbol(name="b", index=2)
        scope = Scope(symbols=[local_symbol_0, local_symbol_1],
                      parent=Scope(symbols=[upper_symbol_0, upper_symbol_1],
                                   parent=Scope(symbols=[root_symbol_0, root_symbol_1],
                                                parent=None)))
        # retrieve all symbols of type SomeSymbol with name 'a'
        result = scope.lookup(symbol_name="a", symbol_type=SomeSymbol)
        self.assertEquals(len(result), 1)
        self.assertEquals(result[0], upper_symbol_0)
        # retrieve all symbols of type SomeSymbol with name 'b'
        result = scope.lookup(symbol_name="b", symbol_type=SomeSymbol)
        self.assertEquals(len(result), 2)
        self.assertEquals(result[0], local_symbol_1)
        self.assertEquals(result[1], root_symbol_1)

    def test_scope_lookup_symbol_by_name_and_type_not_found(self):
        local_symbol_0 = Symbol(name="a")
        local_symbol_1 = SomeSymbol(name="b", index=0)
        upper_symbol_0 = SomeSymbol(name="a", index=1)
        upper_symbol_1 = Symbol(name="b")
        root_symbol_0 = Symbol(name="a")
        root_symbol_1 = SomeSymbol(name="b", index=2)
        scope = Scope(symbols=[local_symbol_0, local_symbol_1],
                      parent=Scope(symbols=[upper_symbol_0, upper_symbol_1],
                                   parent=Scope(symbols=[root_symbol_0, root_symbol_1],
                                                parent=None)))
        # retrieve all symbols of type SomeSymbol with name 'c'
        result = scope.lookup(symbol_name="c", symbol_type=SomeSymbol)
        self.assertEquals(len(result), 0)
        # retrieve all symbols of type AnotherSymbol with name 'a'
        result = scope.lookup(symbol_name="a", symbol_type=AnotherSymbol)
        self.assertEquals(len(result), 0)

    def test_scope_lookup_with_default_arguments(self):
        local_symbol_0 = Symbol(name="a")
        local_symbol_1 = SomeSymbol(name="b", index=0)
        upper_symbol_0 = SomeSymbol(name="a", index=1)
        upper_symbol_1 = Symbol(name="b")
        root_symbol_0 = Symbol(name="a")
        root_symbol_1 = SomeSymbol(name="b", index=2)
        scope = Scope(symbols=[local_symbol_0, local_symbol_1],
                      parent=Scope(symbols=[upper_symbol_0, upper_symbol_1],
                                   parent=Scope(symbols=[root_symbol_0, root_symbol_1],
                                                parent=None)))
        # retrieve all symbols of type Symbol with name None
        result = scope.lookup(symbol_name=None, symbol_type=Symbol)
        self.assertEquals(len(result), 6)
        self.assertEquals(result[0], local_symbol_0)
        self.assertEquals(result[1], local_symbol_1)
        self.assertEquals(result[2], upper_symbol_0)
        self.assertEquals(result[3], upper_symbol_1)
        self.assertEquals(result[4], root_symbol_0)
        self.assertEquals(result[5], root_symbol_1)
        # retrieve all symbols of type Symbol with name ''
        result = scope.lookup(symbol_name='', symbol_type=Symbol)
        self.assertEquals(len(result), 6)
        self.assertEquals(result[0], local_symbol_0)
        self.assertEquals(result[1], local_symbol_1)
        self.assertEquals(result[2], upper_symbol_0)
        self.assertEquals(result[3], upper_symbol_1)
        self.assertEquals(result[4], root_symbol_0)
        self.assertEquals(result[5], root_symbol_1)
