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

