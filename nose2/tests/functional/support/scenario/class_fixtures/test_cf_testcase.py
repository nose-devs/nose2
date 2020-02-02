import unittest


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x = 1

    def test_1(self):
        assert self.x

    def test_2(self):
        assert self.x


class Test2(unittest.TestCase):
    def setUp(self):
        self.x = 1

    def test_1(self):
        assert self.x

    def test_2(self):
        assert self.x


class Test3(Test):
    # this has class setup by virtue of inheritting from Test

    def test_3(self):
        assert self.x
