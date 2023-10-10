import unittest
from dataclasses import dataclass
from typing import List, Set

from pylasu.model import Node
from tests.fixtures import box, Item


@dataclass(unsafe_hash=True)
class AW(Node):
    s: str


@dataclass
class BW(Node):
    a: AW
    many_as: List[AW]


@dataclass
class CW(Node):
    a: AW
    many_as: Set[AW]


class ProcessingTest(unittest.TestCase):
    def test_search_by_type(self):
        self.assertEquals(["1", "2", "3", "4", "5", "6"],
                         [i.name for i in box.search_by_type(Item)])
        self.assertEquals(["root", "first", "1", "2", "big", "small", "3", "4", "5", "6"],
                         [n.name for n in box.search_by_type(Node)])

    def test_replace_in_list(self):
        a1 = AW("1")
        a2 = AW("2")
        a3 = AW("3")
        a4 = AW("4")
        b = BW(a1, [a2, a3])
        b.assign_parents()
        a2.replace_with(a4)
        self.assertEquals("4", b.many_as[0].s)
        self.assertEquals(BW(a1, [a4, a3]), b)

    def test_replace_in_set(self):
        a1 = AW("1")
        a2 = AW("2")
        a3 = AW("3")
        a4 = AW("4")
        c = CW(a1, {a2, a3})
        c.assign_parents()
        self.assertRaises(Exception, lambda: a2.replace_with(a4))

    def test_replace_single(self):
        a1 = AW("1")
        a2 = AW("2")
        b = BW(a1, [])
        b.assign_parents()
        a1.replace_with(a2)
        self.assertEquals("2", b.a.s)
