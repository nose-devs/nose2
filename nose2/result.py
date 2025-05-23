import time

from nose2 import events

ERROR = "error"
FAIL = "failed"
SKIP = "skipped"
PASS = "passed"
SUBTEST = "subtest"
__unittest = True


class PluggableTestResult:
    """Test result that defers to plugins.

    All test outcome recording and reporting is deferred to plugins,
    which are expected to implement :func:`startTest`, :func:`stopTest`,
    :func:`testOutcome`, and :func:`wasSuccessful`.

    :param session: Test run session.

    .. attribute :: shouldStop

       When ``True``, test run should stop before running another test.

    """

    def __init__(self, session) -> None:
        self.session = session
        self.shouldStop = False
        # XXX TestCase.subTest expects a result.failfast attribute
        self.failfast = False
        # track whether or not the test actually started
        # (in py3.12.1+ a skipped test is not started)
        self.test_started = False

    def startTest(self, test):
        """Start a test case.

        Fires :func:`startTest` hook.

        """
        event = events.StartTestEvent(test, self, time.time())
        self.session.hooks.startTest(event)
        self.test_started = True

    def stopTest(self, test):
        """Stop a test case.

        Fires :func:`stopTest` hook.

        """
        event = events.StopTestEvent(test, self, time.time())
        self.session.hooks.stopTest(event)

    def addDuration(self, test, elapsed):  # For Python >= 3.12
        pass

    def addError(self, test, err):
        """Test case resulted in error.

        Fires :func:`setTestOutcome` and :func:`testOutcome` hooks.

        """
        event = events.TestOutcomeEvent(test, self, ERROR, err)
        self.session.hooks.setTestOutcome(event)
        self.session.hooks.testOutcome(event)

    def addFailure(self, test, err):
        """Test case resulted in failure.

        Fires :func:`setTestOutcome` and :func:`testOutcome` hooks.

        """
        event = events.TestOutcomeEvent(test, self, FAIL, err)
        self.session.hooks.setTestOutcome(event)
        self.session.hooks.testOutcome(event)

    def addSubTest(self, test, subtest, err):
        """Called at the end of a subtest.

        Fires :func:`setTestOutcome` and :func:`testOutcome` hooks.

        """
        event = events.TestOutcomeEvent(subtest, self, SUBTEST, err)
        self.session.hooks.setTestOutcome(event)
        self.session.hooks.testOutcome(event)

    def addSuccess(self, test):
        """Test case resulted in success.

        Fires :func:`setTestOutcome` and :func:`testOutcome` hooks.

        """
        event = events.TestOutcomeEvent(test, self, PASS, expected=True)
        self.session.hooks.setTestOutcome(event)
        self.session.hooks.testOutcome(event)

    def addSkip(self, test, reason):
        """Test case was skipped.

        Fires :func:`setTestOutcome` and :func:`testOutcome` hooks.

        """
        event = events.TestOutcomeEvent(test, self, SKIP, reason=reason)
        self.session.hooks.setTestOutcome(event)
        self.session.hooks.testOutcome(event)

    def addExpectedFailure(self, test, err):
        """Test case resulted in expected failure.

        Fires :func:`setTestOutcome` and :func:`testOutcome` hooks.

        """
        event = events.TestOutcomeEvent(test, self, FAIL, err, expected=True)
        self.session.hooks.setTestOutcome(event)
        self.session.hooks.testOutcome(event)

    def addUnexpectedSuccess(self, test):
        """Test case resulted in unexpected success.

        Fires :func:`setTestOutcome` and :func:`testOutcome` hooks.

        """
        event = events.TestOutcomeEvent(test, self, PASS)
        self.session.hooks.setTestOutcome(event)
        self.session.hooks.testOutcome(event)

    def wasSuccessful(self):
        """Was test run successful?

        Fires :func:`wasSuccessful` hook, and returns ``event.success``.

        """
        # assume failure; plugins must explicitly declare success
        try:
            return self._success
        except AttributeError:
            event = events.ResultSuccessEvent(self, None)
            self.session.hooks.wasSuccessful(event)
            self._success = event.success
            return self._success

    def stop(self):
        """Stop test run.

        Fires :func:`resultStop` hook, and sets ``self.shouldStop`` to
        ``event.shouldStop``.

        """
        event = events.ResultStopEvent(self, True)
        self.session.hooks.resultStop(event)
        self.shouldStop = event.shouldStop

    def __repr__(self):
        return "<%s>" % self.__class__.__name__
