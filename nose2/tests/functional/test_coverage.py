import os
import os.path
import platform
import sys
import unittest

from nose2.tests._common import FunctionalTestCase, support_file, windows_ci_skip


class TestCoverage(FunctionalTestCase):
    def setUp(self):
        super().setUp()
        try:
            import coverage  # noqa: F401
        except ImportError:
            self.skipTest("coverage required")

    def assertProcOutputPattern(
        self, proc, libname, stats, total_stats=None, assert_exit_status=0
    ):
        """
        - proc: a popen proc to check output on
        - libname: the name of the covered library, to build the output pattern
        - stats: the output format for stats info
        - total_stats: optional, distinct stats format for the TOTAL line
                       defaults to be the same as stats
        """
        if total_stats is None:
            total_stats = stats

        expected = os.path.join(libname, "mod1(.py)?")
        expected = expected.replace("\\", r"\\")
        expected = expected + stats

        stdout, stderr = proc.communicate()

        if assert_exit_status is not None:
            self.assertEqual(assert_exit_status, proc.poll())

        self.assertTestRunOutputMatches(proc, stderr=expected)
        self.assertTestRunOutputMatches(proc, stderr=r"TOTAL\s+" + total_stats)

    def test_run(self):
        # ensure there is no .coverage file at the start of test
        reportfile = support_file("scenario/test_with_module/.coverage")
        try:
            os.remove(reportfile)
        except OSError:
            pass

        proc = self.runIn(
            "scenario/test_with_module", "-v", "--with-coverage", "--coverage=lib/"
        )
        self.assertProcOutputPattern(proc, "lib", r"\s+8\s+5\s+38%")
        self.assertTrue(os.path.exists(reportfile))

    def test_run_coverage_configs(self):
        STATS = r"\s+8\s+5\s+38%\s+1, 7-10"
        TOTAL_STATS = r"\s+8\s+5\s+38%\s"

        proc = self.runIn(
            "scenario/test_coverage_config/coveragerc",
            "-v",
            "--with-coverage",
            "--coverage=covered_lib_coveragerc/",
        )
        self.assertProcOutputPattern(
            proc, "covered_lib_coveragerc", STATS, total_stats=TOTAL_STATS
        )

    # unclear if this failure is a problem with the test context (coverage run
    # of nose2 with faked subprocesses) or if it's a bug in the coverage plugin
    # or mp plugin on that platform
    @unittest.skipIf(
        platform.system() == "Darwin" and sys.version_info >= (3, 8),
        "FIXME: this test fails on modern pythons on macos",
    )
    @windows_ci_skip
    def test_run_with_mp(self):
        # this test needs to be done with nose2 config because (as of 2019-12)
        # multiprocessing does not allow each test process to pick up on
        # command line arguments

        # run with 4 processes -- this will fail if `coverage` isn't running in
        # a "parallel" mode (with a "data suffix" set and combining results for
        # reporting)
        proc = self.runIn(
            "scenario/test_coverage_config/nose2cfg",
            "-v",
            "--plugin=nose2.plugins.mp",
            "-N",
            "4",
        )
        self.assertProcOutputPattern(
            proc,
            "covered_lib_nose2cfg",
            r"\s+8\s+5\s+38%\s+1, 7-10",
            total_stats=r"\s+8\s+5\s+38%",
        )

    # FIXME: figure out why this fails and remove @skip
    @unittest.skip("fails in testsuite but passes in real-world conditions")
    def test_measures_imports(self):
        proc = self.runIn(
            "scenario/coverage_of_imports",
            "-v",
            "--with-coverage",
            "--coverage=lib20171102/",
        )
        self.assertProcOutputPattern(proc, "lib20171102", stats=r"\s+3\s+0\s+100%")

    def test_run_coverage_fail_under(self):
        STATS = r"\s+8\s+5\s+38%\s+1, 7-10"
        TOTAL_STATS = r"\s+8\s+5\s+38%\s"

        proc = self.runIn(
            "scenario/coverage_config_fail_under",
            "-v",
            "--with-coverage",
            "--coverage=covered_lib/",
        )
        self.assertProcOutputPattern(
            proc, "covered_lib", STATS, total_stats=TOTAL_STATS, assert_exit_status=1
        )

    def test_run_coverage_fail_under2(self):
        """Check with coverage settings in config, not CLI"""
        STATS = r"\s+8\s+5\s+38%\s+1, 7-10"
        TOTAL_STATS = r"\s+8\s+5\s+38%\s"

        proc = self.runIn("scenario/coverage_config_fail_under2", "-v")
        self.assertProcOutputPattern(
            proc,
            "part_covered_lib",
            STATS,
            total_stats=TOTAL_STATS,
            assert_exit_status=1,
        )
