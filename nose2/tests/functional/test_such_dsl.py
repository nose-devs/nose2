from nose2.tests._common import FunctionalTestCase


class TestSuchDSL(FunctionalTestCase):

    def test_runs_example(self):
        proc = self.runIn(
            'such',
            '-v',
            '--plugin=nose2.plugins.layers')
        self.assertTestRunOutputMatches(proc, stderr='Ran 8 tests')
        self.assertEqual(proc.poll(), 0)
