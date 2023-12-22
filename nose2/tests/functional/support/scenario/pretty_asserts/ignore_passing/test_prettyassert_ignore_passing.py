# flake8: noqa
import unittest


class TestFailAssert(unittest.TestCase):
    def test_failing_assert(self):
        x = True
        y = False
        # fmt: off
        assert x; assert y
        # fmt: on

    def test_failing_assert2(self):
        p = 1
        q = 0
        assert p
        assert q
