import os.path

from nose2.tests._common import FunctionalTestCase


class TestCoverage(FunctionalTestCase):
    def assertProcOutputPattern(self, proc, libname, stats,
                                total_stats=None):
        """
        - proc: a popen proc to check output on
        - libname: the name of the covered library, to build the output pattern
        - stats: the output format for stats info
        - total_stats: optional, distinct stats format for the TOTAL line
                       defaults to be the same as stats
        """
        if total_stats is None:
            total_stats = stats

        expected = os.path.join(libname, 'mod1(.py)?')
        expected = expected.replace('\\', r'\\')
        expected = expected + stats

        stdout, stderr = proc.communicate()

        self.assertTestRunOutputMatches(
            proc,
            stderr=expected)
        self.assertTestRunOutputMatches(
            proc,
            stderr='TOTAL\s+' + total_stats)

    def test_run(self):
        proc = self.runIn(
            'scenario/test_with_module',
            '-v',
            '--with-coverage',
            '--coverage=lib/'
        )
        self.assertProcOutputPattern(proc, 'lib', '\s+8\s+5\s+38%')

    def test_run_coverage_configs(self):
        STATS = '\s+8\s+5\s+38%\s+1, 7-10'
        TOTAL_STATS = '\s+8\s+5\s+38%\s'

        proc = self.runIn(
            'scenario/test_coverage_config/coveragerc',
            '-v',
            '--with-coverage',
            '--coverage=covered_lib_coveragerc/'
        )
        self.assertProcOutputPattern(proc, 'covered_lib_coveragerc', STATS,
                                     total_stats=TOTAL_STATS)

        proc = self.runIn(
            'scenario/test_coverage_config/nose2cfg',
            '-v',
            '--with-coverage',
            '--coverage=covered_lib_nose2cfg/'
        )
        self.assertProcOutputPattern(proc, 'covered_lib_nose2cfg', STATS,
                                     total_stats=TOTAL_STATS)
