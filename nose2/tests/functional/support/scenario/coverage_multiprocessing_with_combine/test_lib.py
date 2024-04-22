import unittest

from lib.mod1 import method


class TestLib(unittest.TestCase):
    def test1(self):
        self.assertEqual(method(), True)
