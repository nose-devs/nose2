import unittest

THINGS = []


def setUpModule():
    THINGS.append(1)


def tearDownModule():
    while THINGS:
        THINGS.pop()


class Test(unittest.TestCase):
    def test_1(self):
        assert THINGS, "setup didn't run"

    def test_2(self):
        assert THINGS, "setup didn't run"
