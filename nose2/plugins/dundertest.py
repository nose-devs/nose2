"""
This plugin implements :func:`startTestRun`, which excludes all test objects
that define a ``__test__`` attribute that evaluates to ``False``.
"""
from unittest import TestSuite

from nose2 import events

__unittest = True


class DunderTestFilter(events.Plugin):
    """
    Exclude all tests defining a ``__test__`` attribute that evaluates to ``False``.
    """

    alwaysOn = True

    def startTestRun(self, event):
        """
        Recurse :attr:`event.suite` and remove all test suites and test cases
        that define a ``__test__`` attribute that evaluates to ``False``.
        """
        self.removeNonTests(event.suite)

    def removeNonTests(self, suite):
        for test in list(suite):
            if not getattr(test, "__test__", True):
                suite._tests.remove(test)
            elif isinstance(test, TestSuite):
                self.removeNonTests(test)
