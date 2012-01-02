"""
This module contains some code copied from unittest2/runner.py and other
code developed in reference to that module and others within unittest2.

unittest2 is Copyright (c) 2001-2010 Python Software Foundation; All
Rights Reserved. See: http://docs.python.org/license.html

"""
import time

from nose2 import events, result


class PluggableTestRunner(object):
    resultClass = result.PluggableTestResult

    def __init__(self, session):
        self.session = session

    def run(self, test):
        result = self._makeResult()
        executor = lambda suite, result: suite(result)
        startTime = time.time()
        event = events.StartTestRunEvent(self, test, result, startTime, executor)
        self.session.hooks.startTestRun(event)

        # allows startTestRun to modify test suite
        test = event.suite
        # ... and test execution
        executor = event.executeTests
        try:
            if not event.handled:
                executor(test, result)
        finally:
            stopTime = time.time()
            timeTaken = stopTime - startTime
            event = events.StopTestRunEvent(self, result, stopTime, timeTaken)
            self.session.hooks.stopTestRun(event)
        return result

    def _makeResult(self):
        result = self.resultClass(self.session)
        event = events.ResultCreatedEvent(result)
        self.session.hooks.resultCreated(event)
        return event.result
