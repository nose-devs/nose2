from nose2.tests._common import FunctionalTestCase


class TestSuchDSL(FunctionalTestCase):
    def test_runs_example(self):
        proc = self.runIn(
            'such',
            '-v',
            '--plugin=nose2.plugins.layers',
            'test_such')
        self.assertTestRunOutputMatches(proc, stderr='Ran 9 tests')
        self.assertEqual(proc.poll(), 0, proc.stderr.getvalue())

    def test_load_top_level_by_name(self):
        proc = self.runIn(
            'such',
            '-v',
            '--plugin=nose2.plugins.layers',
            'test_such.A system with complex setup.should do something')
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertEqual(proc.poll(), 0, proc.stderr.getvalue())

    def test_load_sublayer_test_by_name(self):
        proc = self.runIn(
            'such',
            '-v',
            '--plugin=nose2.plugins.layers',
            'test_such.having an expensive fixture.'
            'should do more things')
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertEqual(proc.poll(), 0, proc.stderr.getvalue())

    def test_regression_tests_with_the_same_having_description_under_different_fixtures_in_the_same_module_should_be_run(
            self):
        proc = self.runIn(
            'such',
            '-v',
            '--plugin=nose2.plugins.layers',
            'test_regression_same_havings')
        self.assertTestRunOutputMatches(proc, stderr='Ran 2 test')
        self.assertEqual(proc.poll(), 0, proc.stderr.getvalue())
