import re

from . import TestCase


class TestLogcaptureOutputIncluded(TestCase):
    def test_layout2(self):
        match = re.compile('>> begin captured logging <<')
        self.assertTestRunOutputMatches(
            self.runIn('layout2'),
            stderr=match)
