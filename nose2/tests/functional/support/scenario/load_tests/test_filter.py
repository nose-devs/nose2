import unittest


class TestCase(unittest.TestCase):
    def test_a(self):
        pass

    def test_b(self):
        pass

    def test_c(self):
        pass


def load_tests(loader, tests, pattern):
    del tests._tests[0]._tests[1]
    return tests
