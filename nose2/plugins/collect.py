import time
from unittest2 import Plugin, TestSuite
from unittest2.events import hooks, StartTestEvent, TestReport


class CollectOnly(Plugin):
    configSection = 'collect-only'
    commandLineSwitch = (None, 'collect-only',
                         'Collect and output test names, do not run any tests')

    def startTestRun(self, event):
        event.executeTests = self.collectTests

    def collectTests(self, suite, result):
        for test in suite:
            if isinstance(test, TestSuite):
                self.collectTests(test, result)
                continue
            startTime = time.time()
            event = StartTestEvent(self, result, startTime)
            hooks.startTest(event)
            result.startTest(test)
            stopTime = time.time()
            timeTaken = stopTime - startTime
            event = TestReport(self, result, stopTime, timeTaken,
                               'passed', None, None, None)
            event.setOutcome('collected', 'passed', '.', 'x')
            hooks.createReport(event)
            hooks.stopTest(event)
            result.addSuccess(test)

