from nose2.events import Plugin
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
            result.startTest(test)
            result.addSuccess(test)
            result.stopTest(test)

