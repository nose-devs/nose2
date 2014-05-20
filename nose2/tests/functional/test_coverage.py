from nose2.tests._common import FunctionalTestCase


class TestCoverage(FunctionalTestCase):
    def test_run(self):
        proc = self.runIn(
            'scenario/test_with_module',
            '-v',
            '--with-coverage',
            '--coverage=lib/'
        )
        stdout, stderr = proc.communicate()
        self.assertTestRunOutputMatches(proc, stderr='lib/mod1           8      5    38%')
        self.assertTestRunOutputMatches(proc, stderr='TOTAL              8      5    38%')
