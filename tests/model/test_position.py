import unittest

from pylasu.model import Point

START_LINE = 1
START_COLUMN = 0
START_POINT = Point(START_LINE, START_COLUMN)


class PositionTest(unittest.TestCase):
    def test_point_compare(self):
        p0 = START_POINT
        p1 = Point(1, 1)
        p2 = Point(1, 100)
        p3 = Point(2, 90)

        self.assertFalse(p0 < p0)
        self.assertTrue(p0 <= p0)
        self.assertTrue(p0 >= p0)
        self.assertFalse(p0 > p0)

        self.assertTrue(p0 < p1)
        self.assertTrue(p0 <= p1)
        self.assertFalse(p0 >= p1)
        self.assertFalse(p0 > p1)

        self.assertTrue(p0 < p2)
        self.assertTrue(p0 <= p2)
        self.assertFalse(p0 >= p2)
        self.assertFalse(p0 > p2)

        self.assertTrue(p0 < p3)
        self.assertTrue(p0 <= p3)
        self.assertFalse(p0 >= p3)
        self.assertFalse(p0 > p3)

        self.assertTrue(p1 < p2)
        self.assertTrue(p1 <= p2)
        self.assertFalse(p1 >= p2)
        self.assertFalse(p1 > p2)

        self.assertTrue(p1 < p3)
        self.assertTrue(p1 <= p3)
        self.assertFalse(p1 >= p3)
        self.assertFalse(p1 > p3)

    def test_is_before(self):
        p0 = START_POINT
        p1 = Point(1, 1)
        p2 = Point(1, 100)
        p3 = Point(2, 90)

        self.assertFalse(p0.is_before(p0))
        self.assertTrue(p0.is_before(p1))
        self.assertTrue(p0.is_before(p2))
        self.assertTrue(p0.is_before(p3))

        self.assertFalse(p1.is_before(p0))
        self.assertFalse(p1.is_before(p1))
        self.assertTrue(p1.is_before(p2))
        self.assertTrue(p1.is_before(p3))

        self.assertFalse(p2.is_before(p0))
        self.assertFalse(p2.is_before(p1))
        self.assertFalse(p2.is_before(p2))
        self.assertTrue(p2.is_before(p3))

        self.assertFalse(p3.is_before(p0))
        self.assertFalse(p3.is_before(p1))
        self.assertFalse(p3.is_before(p2))
        self.assertFalse(p3.is_before(p3))
