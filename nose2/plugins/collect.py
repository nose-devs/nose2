import time

from nose2.events import Plugin, StartTestEvent, TestReport
from nose2.compat import unittest


class CollectOnly(Plugin):
    """TODO: document"""

    configSection = 'collect-only'
    commandLineSwitch = (None, 'collect-only',
                         'Collect and output test names, do not run any tests')

    def startTestRun(self, event):
        event.executeTests = self.collectTests

    def collectTests(self, suite, result):
        for test in suite:
            if isinstance(test, unittest.TestSuite):
                self.collectTests(test, result)
                continue
            startTime = time.time()
            event = StartTestEvent(self, result, startTime)
            self.hooks.startTest(event)
            result.startTest(test)
            stopTime = time.time()
            timeTaken = stopTime - startTime
            event = TestReport(self, result, stopTime, timeTaken,
                               'passed', None, None, None)
            event.setOutcome('collected', 'passed', '.', 'x')
            self.hooks.createReport(event)
            self.hooks.stopTest(event)
            result.addSuccess(test)

