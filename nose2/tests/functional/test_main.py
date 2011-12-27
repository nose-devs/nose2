from nose2.compat import unittest
from nose2.tests.functional import run_nose2


class TestPluggableTestProgram(unittest.TestCase):

    def test_run_in_empty_dir_succeeds(self):
        retcode, output, err = run_nose2(cwd='scenario/no_tests')
        self.assertEqual(retcode, 0)
