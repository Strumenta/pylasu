import dataclasses
import unittest
from typing import List

from pylasu.model import Node, Position, Point
from pylasu.model.reflection import Multiplicity
from pylasu.model.naming import ReferenceByName, Named, Scope, Symbol


@dataclasses.dataclass
class SomeNode(Node, Named):
    foo = 3
    bar: int = dataclasses.field(init=False)
    __private__ = 4
    ref: Node = None
    multiple: List[Node] = dataclasses.field(default_factory=list)

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
        node = Node().with_position(Position(Point(1, 0), Point(2, 1)))
        self.assertEqual(Position(Point(1, 0), Point(2, 1)), node.position)
        node = SomeNode("").with_position(Position(Point(1, 0), Point(2, 1)))
        self.assertEqual(Position(Point(1, 0), Point(2, 1)), node.position)

    def test_node_properties(self):
        node = SomeNode("n").with_position(Position(Point(1, 0), Point(2, 1)))
        self.assertIsNotNone(next(n for n in node.properties if n.name == 'foo'))
        self.assertIsNotNone(next(n for n in node.properties if n.name == 'bar'))
        self.assertIsNotNone(next(n for n in node.properties if n.name == "name"))
        with self.assertRaises(StopIteration):
            next(n for n in node.properties if n.name == '__private__')
        with self.assertRaises(StopIteration):
            next(n for n in node.properties if n.name == 'non_existent')
        with self.assertRaises(StopIteration):
            next(n for n in node.properties if n.name == 'properties')
        with self.assertRaises(StopIteration):
            next(n for n in node.properties if n.name == "origin")

    def test_scope_lookup_0(self):
        """Symbol found in local scope with name and default type"""
        local_symbol = SomeSymbol(name='a', index=0)
        scope = Scope(symbols={'a': [local_symbol]}, parent=Scope(symbols={'a': [SomeSymbol(name='a', index=1)]}))
        result = scope.lookup(symbol_name='a')
        self.assertEqual(result, local_symbol)
        self.assertIsInstance(result, Symbol)

    def test_scope_lookup_1(self):
        """Symbol found in upper scope with name and default type"""
        upper_symbol = SomeSymbol(name='a', index=0)
        scope = Scope(symbols={'b': [SomeSymbol(name='b', index=0)]}, parent=Scope(symbols={'a': [upper_symbol]}))
        result = scope.lookup(symbol_name='a')
        self.assertEqual(result, upper_symbol)
        self.assertIsInstance(result, Symbol)

    def test_scope_lookup_2(self):
        """Symbol not found with name and default type"""
        scope = Scope(symbols={'b': [SomeSymbol(name='b', index=0)]},
                      parent=Scope(symbols={'b': [SomeSymbol(name='b', index=1)]}))
        result = scope.lookup(symbol_name='a')
        self.assertIsNone(result)

    def test_scope_lookup_3(self):
        """Symbol found in local scope with name and type"""
        pass

    def test_scope_lookup_4(self):
        """Symbol found in upper scope with name and type"""
        upper_symbol = SomeSymbol(name='a', index=0)
        scope = Scope(symbols={'b': [SomeSymbol(name='b', index=0)]}, parent=Scope(symbols={'a': [upper_symbol]}))
        result = scope.lookup(symbol_name='a', symbol_type=SomeSymbol)
        self.assertEqual(result, upper_symbol)
        self.assertIsInstance(result, SomeSymbol)

    def test_scope_lookup_5(self):
        """Symbol found in upper scope with name and type (local with different type)"""
        upper_symbol = SomeSymbol(name='a', index=0)
        scope = Scope(symbols={'a': [AnotherSymbol(name='a', index=0)]}, parent=Scope(symbols={'a': [upper_symbol]}))
        result = scope.lookup(symbol_name='a', symbol_type=SomeSymbol)
        self.assertEqual(result, upper_symbol)
        self.assertIsInstance(result, SomeSymbol)

    def test_scope_lookup_6(self):
        """Symbol not found with name and type (different name)"""
        scope = Scope(symbols={'b': [SomeSymbol(name='b', index=0)]},
                      parent=Scope(symbols={'b': [SomeSymbol(name='b', index=1)]}))
        result = scope.lookup(symbol_name='a', symbol_type=SomeSymbol)
        self.assertIsNone(result)

    def test_scope_lookup_7(self):
        """Symbol not found with name and type (different type)"""
        scope = Scope(symbols={'a': [SomeSymbol(name='a', index=0)]},
                      parent=Scope(symbols={'a': [SomeSymbol(name='a', index=1)]}))
        result = scope.lookup(symbol_name='a', symbol_type=AnotherSymbol)
        self.assertIsNone(result)

    def test_scope_case_insensitive_lookup(self):
        local_symbol = SomeSymbol(name='a', index=0)
        scope = Scope(symbols={'a': [local_symbol]}, parent=Scope(symbols={'a': [SomeSymbol(name='a', index=1)]}))
        result = scope.lookup(symbol_name='A', case_insensitive=True)
        self.assertEqual(result, local_symbol)
        self.assertIsInstance(result, Symbol)

    def test_node_properties_meta(self):
        pds = [pd for pd in sorted(SomeNode.node_properties, key=lambda x: x.name)]
        self.assertEqual(5, len(pds))
        self.assertEqual("bar", pds[0].name)
        self.assertFalse(pds[0].provides_nodes)
        self.assertEqual("foo", pds[1].name)
        self.assertFalse(pds[1].provides_nodes)
        self.assertEqual("multiple", pds[2].name)
        self.assertTrue(pds[2].provides_nodes)
        self.assertEqual(Multiplicity.MANY, pds[2].multiplicity)
        self.assertEqual("name", pds[3].name)
        self.assertFalse(pds[3].provides_nodes)
        self.assertEqual("ref", pds[4].name)
        self.assertTrue(pds[4].provides_nodes)