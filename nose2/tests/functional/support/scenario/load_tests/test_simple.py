import unittest


class TestCase(unittest.TestCase):
    def test_a(self):
        pass

    def test_b(self):
        pass

    def test_c(self):
        pass


def load_tests(loader, tests, pattern):
    class InnerTest(unittest.TestCase):
        def test_d(self):
            pass

    tests.addTest(InnerTest("test_d"))
    return tests
