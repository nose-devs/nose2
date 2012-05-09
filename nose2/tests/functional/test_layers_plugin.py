from nose2.tests._common import FunctionalTestCase


class TestLayers(FunctionalTestCase):

    def test_runs_layer_fixtures(self):
        proc = self.runIn(
            'scenario/layers',
            '-v',
            '--plugin=nose2.plugins.layers')
        self.assertTestRunOutputMatches(proc, stderr='Ran 8 tests')
        self.assertEqual(proc.poll(), 0)

    def test_scenario_fails_without_plugin(self):
        proc = self.runIn(
            'scenario/layers',
            '-v')
        self.assertTestRunOutputMatches(proc, stderr='Ran 8 tests')
        self.assertTestRunOutputMatches(proc, stderr=r'FAILED \(failures=7\)')
        self.assertEqual(proc.poll(), 1)

    def test_layer_reporter_output(self):
        proc = self.runIn(
            'scenario/layers',
            '-v',
            '--plugin=nose2.plugins.layers',
            '--layer-reporter')
        expect = r"""test \(test_layers.NoLayer\) ... ok
Base
  test \(test_layers.Outer\) ... ok
  LayerD
    test \(test_layers.InnerD\) ... ok
  LayerA
    test \(test_layers.InnerA\) ... ok
  LayerB
    LayerB_1
      test \(test_layers.InnerB_1\) ... ok
    LayerC
      test \(test_layers.InnerC\) ... ok
      test2 \(test_layers.InnerC\) ... ok
    LayerA_1
      test \(test_layers.InnerA_1\) ... ok""".split("\n")
        self.assertTestRunOutputMatches(proc, stderr='Ran 8 tests')
        for line in expect:
            self.assertTestRunOutputMatches(proc, stderr=line)
        self.assertEqual(proc.poll(), 0)

    def test_layer_reporter_error_output(self):
        proc = self.runIn(
            'scenario/layers_with_errors',
            '--plugin=nose2.plugins.layers',
            '--layer-reporter')
        expect = [
            r'ERROR: fixture with a value test_err '
            '\(test_layers_with_errors.Test\)',
            'ERROR: A test scenario with errors should check for an attribute '
            'that does not exist and raise an error',
            r'FAIL: fixture with a value test_fail '
            '\(test_layers_with_errors.Test\)',
            'FAIL: A test scenario with errors should check that value == 2 '
            'and fail']
        for line in expect:
            self.assertTestRunOutputMatches(proc, stderr=line)
        self.assertEqual(proc.poll(), 1)
