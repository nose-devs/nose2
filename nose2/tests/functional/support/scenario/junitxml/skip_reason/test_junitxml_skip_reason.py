import unittest


class Test(unittest.TestCase):
    @unittest.skip("ohai")
    def test(self):
        pass
