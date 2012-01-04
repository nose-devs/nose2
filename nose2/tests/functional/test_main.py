from nose2.tests._common import FunctionalTestCase


class TestPluggableTestProgram(FunctionalTestCase):
    def test_run_in_empty_dir_succeeds(self):
        proc = self.runIn('scenario/no_tests')
        stdout, stderr = proc.communicate()
        self.assertEqual(proc.poll(), 0, stderr)
