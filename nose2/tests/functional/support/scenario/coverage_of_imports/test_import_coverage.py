import unittest

from lib20171102.mod1 import foo, func


class TestCase(unittest.TestCase):
    def test1(self):
        self.assertEqual(foo, 1)

    def test2(self):
        self.assertEqual(func(), 2)
