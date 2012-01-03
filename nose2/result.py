import time

from nose2 import events


ERROR = 'error'
FAIL = 'failed'
SKIP = 'skipped'
PASS = 'passed'
__unittest = True


class PluggableTestResult(object):
    """Test result that defers to plugins.

    All test outcome recording and reporting is deferred to plugins,
    which are expected to implement startTest, stopTest, testOutcome,
    and wasSuccessful.

    """
    def __init__(self, session):
        self.session = session
        self.shouldStop = False

    def startTest(self, test):
        event = events.StartTestEvent(test, self, time.time())
        self.session.hooks.startTest(event)

    def stopTest(self, test):
        event = events.StopTestEvent(test, self, time.time())
        self.session.hooks.stopTest(event)

    def addError(self, test, err):
        event = events.TestOutcomeEvent(test, self, ERROR, err)
        self.session.hooks.testOutcome(event)

    def addFailure(self, test, err):
        event = events.TestOutcomeEvent(test, self, FAIL, err)
        self.session.hooks.testOutcome(event)

    def addSuccess(self, test):
        event = events.TestOutcomeEvent(test, self, PASS)
        self.session.hooks.testOutcome(event)

    def addSkip(self, test, reason):
        event = events.TestOutcomeEvent(test, self, SKIP)
        self.session.hooks.testOutcome(event)

    def addExpectedFailure(self, test, err):
        event = events.TestOutcomeEvent(test, self, FAIL, err, expected=True)
        self.session.hooks.testOutcome(event)

    def addUnexpectedSuccess(self, test):
        event = events.TestOutcomeEvent(test, self, PASS, expected=False)
        self.session.hooks.testOutcome(event)

    def wasSuccessful(self):
        # assume failure, plugins must affirmatively declare success
        try:
            return self._success
        except AttributeError:
            event = events.ResultSuccessEvent(self, False)
            self.session.hooks.wasSuccessful(event)
            self._success = event.success
            return self._success

    def stop(self):
        event = events.ResultStopEvent(self, True)
        self.session.hooks.resultStop(event)
        self.shouldStop = event.shouldStop
