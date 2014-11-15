from itertools import permutations
from src.geometry import Rectangle, group_rectangles

__author__ = 'Marek'

import unittest


class GeometryTestCase(unittest.TestCase):
    def test_contains_point(self):
        r = Rectangle(10, 10, 10, 10)

        self.assertEquals(True,  r.contains_point((10, 10,)))
        self.assertEquals(True,  r.contains_point((20, 10,)))
        self.assertEquals(True,  r.contains_point((10, 20,)))
        self.assertEquals(True,  r.contains_point((20, 20,)))
        self.assertEquals(True,  r.contains_point((15, 15,)))

        self.assertEquals(False, r.contains_point((0, 0,)))
        self.assertEquals(False, r.contains_point((0, 15,)))
        self.assertEquals(False, r.contains_point((0, 30,)))

        self.assertEquals(False, r.contains_point((15, 0,)))
        self.assertEquals(False, r.contains_point((15, 30,)))

        self.assertEquals(False, r.contains_point((30, 0,)))
        self.assertEquals(False, r.contains_point((30, 15,)))
        self.assertEquals(False, r.contains_point((30, 30,)))

    def test_is_inside(self):
        a = Rectangle(10, 10, 10, 10)
        self.assertTrue(a.is_inside(a)), self.assertTrue(a.is_overlaying(a))

        b = Rectangle(12, 12, 6, 6)
        self.assertTrue(b.is_inside(a)), self.assertTrue(a.is_overlaying(b))

        b = Rectangle(8, 8, 12, 12)
        self.assertTrue(a.is_inside(b)), self.assertTrue(b.is_overlaying(a))

        r_list = [
            Rectangle(0, 0, 4, 4),
            Rectangle(12, 0, 4, 4),
            Rectangle(22, 0, 4, 4),

            Rectangle(0, 12, 4, 4),
            Rectangle(22, 12, 4, 4),

            Rectangle(0, 22, 4, 4),
            Rectangle(12, 22, 4, 4),
            Rectangle(22, 22, 4, 4),
        ]

        for b in r_list:
            self.assertFalse(a.is_inside(b))
            self.assertFalse(b.is_inside(a))
            self.assertFalse(a.is_overlaying(b))
            self.assertFalse(b.is_overlaying(a))

    def test_is_colliding_with(self):
        a = Rectangle(10, 10, 10, 10)
        r_list = [
            Rectangle(0, 0, 4, 4),
            Rectangle(12, 0, 4, 4),
            Rectangle(22, 0, 4, 4),

            Rectangle(0, 12, 4, 4),
            Rectangle(22, 12, 4, 4),

            Rectangle(0, 22, 4, 4),
            Rectangle(12, 22, 4, 4),
            Rectangle(22, 22, 4, 4),
        ]
        for b in r_list:
            self.assertFalse(a.is_colliding_with(b))
            self.assertFalse(b.is_colliding_with(a))

        r_list = [
            Rectangle( 8, 8, 4, 4),
            Rectangle(12, 8, 4, 4),
            Rectangle(18, 8, 4, 4),

            Rectangle( 8, 12, 4, 4),
            Rectangle(12, 12, 4, 4),
            Rectangle(18, 12, 4, 4),

            Rectangle( 8, 18, 4, 4),
            Rectangle(12, 18, 4, 4),
            Rectangle(18, 18, 4, 4),
        ]
        for b in r_list:
            self.assertTrue(a.is_colliding_with(b))
            self.assertTrue(b.is_colliding_with(a))

    def test_is_colliding_with2(self):
        a = Rectangle(10, 10, 10, 10)
        r_list = [
            Rectangle(0, 8, 30, 4),
            Rectangle(0, 12, 30, 6),
            Rectangle(0, 18, 30, 6),

            Rectangle(8,  0, 4, 30),
            Rectangle(12, 0, 6, 30),
            Rectangle(18, 0, 6, 30),
        ]
        for b in r_list:
            self.assertTrue(a.is_colliding_with(b), repr(a) + " is not colliding with " + repr(b))
            self.assertTrue(b.is_colliding_with(a), repr(b) + " is not colliding with " + repr(a))

    def test_group_rectangles_no_groups(self):
        r_list = [
            Rectangle( 8, 8, 4, 4),
            Rectangle(12, 8, 4, 4),
            Rectangle(18, 8, 4, 4),

            Rectangle( 8, 12, 4, 4),
            Rectangle(18, 12, 4, 4),

            Rectangle( 8, 18, 4, 4),
            Rectangle(12, 18, 4, 4),
            Rectangle(18, 18, 4, 4),
        ]
        for perm in permutations(r_list):
            result = group_rectangles(perm)
            self.assertEquals(8, len(result), "Expected 8 but it was %d" %(len(result)) + ", " + repr(result))

    def test_group_rectangles_groups(self):
        r_list = [
            Rectangle(10, 10, 10, 10),
            Rectangle(12, 12, 4, 4),
            Rectangle(0, 0, 30, 30),
        ]
        for perm in permutations(r_list):
            result = group_rectangles(perm)
            self.assertEquals(1, len(result), "Expected 1 but it was %d" %(len(result)) + ", " + repr(result))