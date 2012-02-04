import logging
import multiprocessing
import time
import unittest

from nose2 import events

log = logging.getLogger(__name__)


class MultiProcess(events.Plugin):
    configSection = 'multiprocess'

    def __init__(self):
        self.addArgument(self.setProcs, 'N', '--processes', '# o procs')
        self.testRunTimeout = self.config.as_float('test-run-timeout', 60.0)

    def setProcs(self, num):
        self.procs = int(num[0]) # FIXME
        self.register()

    ## pluginsLoaded -- add mp hooks
    def pluginsLoaded(self, plugins):
        self.session.hooks.addMethod('registerInSubprocess')
        self.session.hooks.addMethod('startSubprocess')
        self.session.hooks.addMethod('stopSubprocess')

    def startTestRun(self, event):
        event.executeTests = self._runmp

    def _runmp(self, test, result):
        flat = iter(self._flatten(test))
        procs = self._startProcs()
        # distribute tests more-or-less evenly among processes
        self.results = {}
        for caseid, case in flat:
            for proc, conn in procs:
                self.results[caseid] = None
                conn.send(caseid)
                caseid = flat.next()
        # poll pipes for test results
        while self._waiting():
            for proc, conn in procs:
                # XXX proc could be dead
                # XXX have a timeout of 1 second once per loop
                # to avoid busy waiting?
                if conn.poll():
                    remote_events = conn.recv()
                    # XXX
                    # replay result calls into my result
                    for (hook, event) in remote_events:
                        self._localize(event)
                        getattr(self.session.hooks, hook)(event)
            time.sleep(.1)

    def _startProcs(self):
        # XXX create session export
        session_export = self._exportSession()
        procs = []
        for i in range(0, self.procs):
            parent_conn, child_conn = multiprocessing.Pipe()
            proc = multiprocessing.Process(
                target=procserver, args=(session_export, child_conn))
            proc.start()
            procs.append((proc, parent_conn))
        return procs

    def _flatten(self, suite):
        # XXX
        # really: examine suite tests to find out if they have class
        # or module fixtures and group them that way into names
        # of test classes or modules
        flat = []
        for test in suite:
            if isinstance(test, unittest.TestSuite):
                flat.extend(self._flatten(test))
            else:
                flat.append(test.id())
        return flat

    def _waiting(self):
        for r in self.results.values():
            if r is None:
                return True
        return False

    def _localize(self, event):
        # XXX set loader, case, result etc to local ones, if present in event
        # (event case will be just the id)
        # (traceback in exc_info if any won't be real!)
        pass

    def _exportSession(self):
        # argparse isn't pickleable
        # no plugin instances
        # no hooks
        export = {'config': self.session.config,
                  'verbosity': self.session.verbosity,
                  'startDir': self.session.startDir,
                  'topLevelDir': self.session.topLevelDir,
                  # XXX classes or modules?
                  'pluginClasses': []}
        # XXX fire registerInSubprocess -- add those plugin classes
        # (classes must be pickleable!)
        return export


def procserver(session_export, conn):
    rlog = logging.getLogger('%s:remote' % __name__)
    # make a real session from the "session" we got
    # init logging system
    # loader, result
    # load and register plugins
    # loop: read test id from conn
    #   fire load tests by name
    #   make recording test result
    #   run test(s) returned by hook
    #   send results back on conn -- list of (testid, hook, event) tuples


# XXX not recording result, recording *hook*
# class set in the session in procserver
# case(res)
# send back session.hooks.flush()

def run_test(case):
    res = RecordingResult()
    case(res)
    return res.events()


class RecordingResult(object):
    def __init__(self):
        self._events = []

    def events(self):
        return self._events

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
