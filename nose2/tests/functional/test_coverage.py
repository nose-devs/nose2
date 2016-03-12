import os.path
import platform
from nose2.compat import unittest

from nose2.tests._common import FunctionalTestCase


class TestCoverage(FunctionalTestCase):
    @unittest.skipIf(
        platform.python_version_tuple()[:2] == ('3', '2'),
        'coverage package does not support python 3.2')
    def test_run(self):
        proc = self.runIn(
            'scenario/test_with_module',
            '-v',
            '--with-coverage',
            '--coverage=lib/'
        )
        STATS = '\s+8\s+5\s+38%'
        expected = os.path.join('lib', 'mod1(.py)?')
        expected = expected.replace('\\', r'\\')
        expected = expected + STATS
        stdout, stderr = proc.communicate()
        self.assertTestRunOutputMatches(
            proc,
            stderr=expected)
        self.assertTestRunOutputMatches(
            proc,
            stderr='TOTAL\s+' + STATS)
