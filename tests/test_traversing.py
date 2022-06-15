import unittest

from tests.fixtures import box


class TraversingTest(unittest.TestCase):
    def test_walk_depth_first(self):
        self.assertEqual(["root", "first", "1", "2", "big", "small", "3", "4", "5", "6"],
                         [n.name for n in box.walk()])

    def test_walk_leaves_first(self):
        self.assertEqual(["1", "first", "2", "3", "4", "5", "small", "big", "6", "root"],
                         [n.name for n in box.walk_leaves_first()])
