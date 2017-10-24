import unittest

from covered_lib_coveragerc import mod1


class TestLib(unittest.TestCase):
    def test1(self):
        self.assertEqual(mod1.covered_func(), 9)
