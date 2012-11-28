from nose2.compat import unittest


class L1(object):
    @classmethod
    def setUp(cls):
        print('L1setUp')

    @classmethod
    def testSetUp(cls):
        print('L1testSetUp')

    @classmethod
    def tearDown(cls):
        print('L1tearDown')

    @classmethod
    def testTearDown(cls):
        print('L1testTearDown')


class L2(L1):
    @classmethod
    def setUp(cls):
        print('L2setUp')

    @classmethod
    def testSetUp(cls):
        print('L2testSetUp')


# L1 tearDown should only run once
class T1(unittest.TestCase):
    layer = L2

    def test1(self):
        pass

    def test2(self):
        pass
