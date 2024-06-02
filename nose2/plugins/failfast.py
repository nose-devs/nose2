"""
Stop the test run after the first error or failure.

This plugin implements :func:`testOutcome` and sets
``event.result.shouldStop`` if it sees an outcome with exc_info that
is not expected.

"""

from nose2 import events

__unittest = True


class FailFast(events.Plugin):
    """Stop the test run after error or failure"""

    configSection = "failfast"

    def __init__(self):
        """Initialize failfast as stop and failcount as current count"""
        self.failfast = 0
        self.failcount = 0
        self.addArgument(
            self.setFailFast,
            "F",
            "fail-fast",
            "Stop the test run after the first error or failure (1 = auto)",
        )
        # Number of failures to stop the execution
        self.failfast = self.config.as_int("failures", 0)

    def handleArgs(self, args):
        """Register if fail-fast is >0 in cfg or command-line"""
        if self.failfast > 0:
            self.register()

    def setFailFast(self, num):
        """CB to parse and set failcount"""
        try:
            self.failfast = int(num[0])
        except ValueError:
            # Invalid fastfail argument, has to be integer and greater than 0
            self.failfast = 0

    def resultCreated(self, event):
        """Mark new result"""
        if hasattr(event.result, "failfast"):
            # event.result.failfast = True
            # Set failfast as True when current failure count matches failcount
            if self.failcount >= self.failfast:
                event.result.failfast = True

    def testOutcome(self, event):
        """Stop on unexpected error or failure"""
        if event.exc_info and not event.expected:
            # event.result.shouldStop = True
            # Check if current count reached failcount
            self.failcount += 1
            if self.failcount >= self.failfast:
                event.result.shouldStop = True
