import unittest


class TestWithExpectedFailures(unittest.TestCase):
    @unittest.expectedFailure
    def test_should_fail(self):
        assert False

    @unittest.expectedFailure
    def test_should_pass(self):
        assert True

    def test_whatever(self):
        assert True

    def test_fails(self):
        assert False
