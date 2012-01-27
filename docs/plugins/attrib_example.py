import unittest


class Test(unittest.TestCase):

    def test_fast(self):
        pass
    test_fast.fast = 1
    test_fast.layer = 2
    test_fast.flags = ['blue', 'green']

    def test_faster(self):
        pass
    test_faster.fast = 1
    test_faster.layer = 1
    test_faster.flags = ['red', 'green']

    def test_slow(self):
        pass
    test_slow.fast = 0
    test_slow.slow = 1
    test_slow.layer = 2

    def test_slower(self):
        pass
    test_slower.slow = 1
    test_slower.layer = 3
    test_slower.flags = ['blue', 'red']
