from nose2.compat import unittest
from nose2 import events


class PluggableTestResult(unittest.TestResult):
    def __init__(self, session):
        self.session = session
        self.shouldStop = False

    def startTest(self, test):
        pass

    def stopTest(self, test):
        pass

    def addError(self, test, err):
        pass

    def addFailure(self, test, err):
        pass

    def addSuccess(self, test):
        pass

    def addSkip(self, test, reason):
        pass

    def addExpectedFailure(self, test, err):
        pass

    def addUnexpectedSuccess(self, test):
        pass

    def wasSuccessful(self):
        return True

    def stop(self):
        self.shouldStop = True
