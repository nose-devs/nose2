import unittest


class TestFoo(unittest.TestCase):
    def test_ohnoez(self):
        self.x = 1

        def foo():
            return self

        assert foo().x != self.x
