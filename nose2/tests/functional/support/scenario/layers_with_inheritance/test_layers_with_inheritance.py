import unittest


class L1:
    @classmethod
    def setUp(cls):
        print("L1 setUp")

    @classmethod
    def testSetUp(cls):
        print("L1 testSetUp")

    @classmethod
    def tearDown(cls):
        print("L1 tearDown")

    @classmethod
    def testTearDown(cls):
        print("L1 testTearDown")


class L2(L1):
    @classmethod
    def setUp(cls):
        print("L2 setUp")

    @classmethod
    def testSetUp(cls):
        print("L2 testSetUp")

    @classmethod
    def testTearDown(cls):
        print("L2 testTearDown")


# L1 tearDown should only run once
class T1(unittest.TestCase):
    layer = L2

    def test1(self):
        print("Run test1")

    def test2(self):
        print("Run test2")
