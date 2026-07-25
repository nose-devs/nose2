import unittest


class SkipInSetUpClass(unittest.TestCase):
    """SkipTest from setUpClass should skip the class, not error.

    Regression coverage for issue #373: this was reported as an error
    (an ``_ErrorHolder`` failure) rather than a skip.
    """

    @classmethod
    def setUpClass(cls):
        raise unittest.SkipTest("skipping the whole class")

    def test_not_run_1(self):
        raise AssertionError("setUpClass skipped; this must never run")

    def test_not_run_2(self):
        raise AssertionError("setUpClass skipped; this must never run")


class SkipInSetUpModuleSibling(unittest.TestCase):
    """A normal class in the same module still runs."""

    def test_runs(self):
        self.assertTrue(True)
