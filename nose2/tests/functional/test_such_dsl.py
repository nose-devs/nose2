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

    def test_teardown_fail(self):
        proc = self.runIn('scenario/layers_with_errors',
                          '--plugin=nose2.plugins.layers',
                          '-v',
                          'test_such_teardown_fail')
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test in')
        self.assertTestRunOutputMatches(proc, stderr='ERROR: LayerSuite')
        self.assertTestRunOutputMatches(proc, stderr=r'FAILED \(errors=1\)')
        self.assertTestRunOutputMatches(proc, stderr='Bad Error in such tearDown')

    def test_setup_fail(self):
        proc = self.runIn('scenario/layers_with_errors',
                          '--plugin=nose2.plugins.layers',
                          '-v',
                          'test_such_setup_fail')
        self.assertTestRunOutputMatches(proc, stderr='Ran 0 tests in')
        self.assertTestRunOutputMatches(proc, stderr='ERROR: LayerSuite')
        self.assertTestRunOutputMatches(proc, stderr=r'FAILED \(errors=1\)')
        self.assertTestRunOutputMatches(proc, stderr='Bad Error in such setUp!')

    def test_param_plugin_with_such(self):
        proc = self.runIn('scenario/such_with_params',
                          '--plugin=nose2.plugins.layers',
                          '-v',
                          'such_with_params')
        self.assertTestRunOutputMatches(proc, stderr='Ran 6 tests in')
        self.assertTestRunOutputMatches(proc, stderr='OK')
        self.assertTestRunOutputMatches(proc, stderr='test 0000: should do bar:3')
        self.assertTestRunOutputMatches(proc, stderr='test 0001: should do bar and extra:3')
