import unittest


class TestFoo(unittest.TestCase):
    x = 1

    def test_ohnoez(self):
        x = self
        assert x.x != (self
                       ).x
