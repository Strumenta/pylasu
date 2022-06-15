import unittest

from pylasu.model import Node
from tests.fixtures import box, Item


class ProcessingTest(unittest.TestCase):
    def test_search_by_type(self):
        self.assertEqual(["1", "2", "3", "4", "5", "6"],
                         [i.name for i in box.search_by_type(Item)])
        self.assertEqual(["root", "first", "1", "2", "big", "small", "3", "4", "5", "6"],
                         [n.name for n in box.search_by_type(Node)])
