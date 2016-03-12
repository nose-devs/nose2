from nose2.tests._common import FunctionalTestCase


class TestLoadTestsPlugin(FunctionalTestCase):

    def test_simple(self):
        proc = self.runIn(
            'scenario/load_tests',
            '-v',
            '--plugin=nose2.plugins.loader.loadtests')
        self.assertTestRunOutputMatches(proc, stderr='Ran 6 tests')
        self.assertTestRunOutputMatches(proc, stderr='test_a..test_simple')
        self.assertTestRunOutputMatches(proc, stderr='test_b..test_simple')
        self.assertTestRunOutputMatches(proc, stderr='test_c..test_simple')
        self.assertTestRunOutputMatches(proc, stderr='test_d..test_simple')
        self.assertTestRunOutputMatches(proc, stderr='test_a..test_filter')
        self.assertTestRunOutputMatches(proc, stderr='test_c..test_filter')
        self.assertEqual(proc.poll(), 0)

    def test_package(self):
        proc = self.runIn(
            'scenario/load_tests_pkg',
            '-v',
            '-c='
            'nose2/tests/functional/support/scenario/load_tests_pkg/unittest.cfg',
            '--plugin=nose2.plugins.loader.loadtests')
        self.assertTestRunOutputMatches(proc, stderr='Ran 2 tests')
        self.assertTestRunOutputMatches(
            proc, stderr='test..ltpkg.tests.test_find_these.Test')
        # with python >= 3.5, the test name contains the fully qualified class
        # name, so the regexp has an optional matching part.
        self.assertTestRunOutputMatches(
            proc, stderr='test..ltpkg2.tests(.load_tests.<locals>)?.Test')

    def test_project_directory_inside_package(self):
        proc = self.runIn(
            'scenario/load_tests_pkg/ltpkg/tests',
            '-v',
            '-c='
            'nose2/tests/functional/support/scenario/load_tests_pkg/unittest.cfg',
            '--plugin=nose2.plugins.loader.loadtests')
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertTestRunOutputMatches(
            proc, stderr='test..ltpkg.tests.test_find_these.Test')
