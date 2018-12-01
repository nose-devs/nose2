import unittest


class TestFoo(unittest.TestCase):
    def test_old_assertion(self):
        x = False
        self.assertTrue(x)
