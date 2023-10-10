import unittest

from pylasu.model import pos
from tests.fixtures import box


class TraversingTest(unittest.TestCase):
    def test_walk_within_with_outside_position(self):
        self.assertEquals([], [n.name for n in box.walk_within(pos(15, 1, 15, 1))])

    def test_walk_within_with_root_position(self):
        self.assertEquals(
            ["root", "first", "1", "2", "big", "small", "3", "4", "5", "6"],
            [n.name for n in box.walk_within(box.position)]
        )

    def test_walk_within_with_leaf_position(self):
        self.assertEquals(["6"], [n.name for n in box.walk_within(pos(13, 3, 13, 9))])

    def test_walk_within_with_subtree_position(self):
        self.assertEquals(["small", "3", "4", "5"], [n.name for n in box.walk_within(pos(7, 5, 11, 5))])

    def test_walk_depth_first(self):
        self.assertEquals(
            ["root", "first", "1", "2", "big", "small", "3", "4", "5", "6"],
            [n.name for n in box.walk()]
        )

    def test_walk_leaves_first(self):
        self.assertEquals(
            ["1", "first", "2", "3", "4", "5", "small", "big", "6", "root"],
            [n.name for n in box.walk_leaves_first()]
        )

    def test_walk_descendants(self):
        self.assertEquals(
            ["first", "1", "2", "big", "small", "3", "4", "5", "6"],
            [n.name for n in box.walk_descendants()]
        )

    def test_walk_ancestors(self):
        box.assign_parents()
        item4 = box.contents[2].contents[0].contents[1]
        self.assertEquals(["small", "big", "root"], [n.name for n in item4.walk_ancestors()])
