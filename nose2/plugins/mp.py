import logging
import multiprocessing
import select
import unittest

from nose2 import events, loader, result, runner, session, util

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
        self.cases = {}
        for caseid, case in flat:
            for proc, conn in procs:
                # XXX this is wrong, we need to record each
                # individual case and these could be classes or modules
                self.cases[caseid] = case
                conn.send(caseid)
                caseid = flat.next()

        # None is the 'done' flag
        for proc, conn in procs:
            conn.send(None)

        # wait for results
        rdrs = [conn
                for proc, conn in procs
                if proc.is_alive()]

        while rdrs:
            ready, _, _ = select.select(rdrs, [], [], self.testRunTimeout)
            for conn in ready:
                # XXX proc could be dead
                try:
                    remote_events = conn.recv()
                except EOFError:
                    # probably dead
                    log.warning("Subprocess connection closed unexpectedly")
                    continue # XXX or die?
                # replay events
                for (hook, event) in remote_events:
                    self._localize(event)
                    getattr(self.session.hooks, hook)(event)
            rdrs = [conn
                    for proc, conn in procs
                    if proc.is_alive()]
        for proc, conn in procs:
            conn.close()

    def _startProcs(self):
        # XXX create session export
        session_export = self._exportSession()
        procs = []
        for i in range(0, self.procs):
            parent_conn, child_conn = multiprocessing.Pipe()
            proc = multiprocessing.Process(
                target=procserver, args=(session_export, child_conn))
            proc.daemon = True
            proc.start()
            procs.append((proc, parent_conn))
        return procs

    def _flatten(self, suite):
        # XXX
        # really: examine suite tests to find out if they have class
        # or module fixtures and group them that way into names
        # of test classes or modules
        # ALSO record all test cases in self._cases
        flat = []
        for test in suite:
            if isinstance(test, unittest.TestSuite):
                flat.extend(self._flatten(test))
            else:
                flat.append(test.id())
                self.cases[test.id()] = test
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
        if hasattr(event, 'result'):
            event.result = self.session.testResult
        if hasattr(event, 'loader'):
            event.loaded = self.session.testLoader
        if hasattr(event, 'runner'):
            event.runner = self.session.testRunner
        if hasattr(event, 'case'):
            # remote event.case is the test id
            event.case = self.cases[event.case]

    def _exportSession(self):
        # argparse isn't pickleable
        # no plugin instances
        # no hooks
        export = {'config': self.session.config,
                  'verbosity': self.session.verbosity,
                  'startDir': self.session.startDir,
                  'topLevelDir': self.session.topLevelDir,
                  'logLevel': self.session.logLevel,
                  # XXX classes or modules?
                  'pluginClasses': []}
        # XXX fire registerInSubprocess -- add those plugin classes
        # (classes must be pickleable!)
        event = RegisterInSubprocessEvent() # FIXME should be own event type
        self.session.hooks.registerInSubprocess(event)
        export['pluginClasses'].extend(event.pluginClasses)
        return export


def procserver(session_export, conn):
    rlog = logging.getLogger('%s:remote' % __name__)
    # make a real session from the "session" we got
    ssn = session.Session()
    ssn.argparse = None # FIXME
    ssn.pluginargs = None # FIXME
    ssn.config = session_export['config']
    ssn.hooks = events.RecordingPluginInterface()
    ssn.verbosity = session_export['verbosity']
    ssn.startDir = session_export['startDir']
    ssn.topLevelDir = session_export['topLevelDir']

    # init logging system
    logging.basicConfig(level=session_export['logLevel'])
    loader_ = loader.PluggableTestLoader(ssn)
    ssn.testLoader = loader_
    result_ = result.PluggableTestResult(ssn)
    ssn.testResult = result_
    runner_ = runner.PluggableTestRunner(ssn) # needed??
    ssn.testRunner = runner_
    # load and register plugins
    ssn.plugins = [
        plugin(session=ssn) for plugin in session_export['pluginClasses']]
    rlog.debug("Plugins loaded: %s", ssn.plugins)
    for plugin in ssn.plugins:
        plugin.register()
        rlog.debug("Registered %s in subprocess", plugin)

    event = SubprocessEvent(loader_, result_, runner_, ssn.plugins, conn)
    res = ssn.hooks.startSubprocess(event)
    if event.handled and not res:
        return
    executor = event.executeTests
    for testid in gentests(conn):
        if testid is None:
            break
        test = event.loader.loadTestsFromName(testid)
        if event.handled:
            continue
        # xxx try/except?
        rlog.debug("Execute test %s (%s)", testid, test)
        executor(test, event.result)
        conn.send((testid, ssn.hooks.flush()))
        rlog.debug("Log for %s returned", testid)
    ssn.hooks.stopSubprocess(event)


# test generator
def gentests(conn):
    while True:
        try:
            testid = conn.recv()
            if testid is None:
                return
            yield testid
        except EOFError:
            return


# custom event classes
class SubprocessEvent(events.Event):
    def __init__(self, loader, result, runner, plugins, connection, **metadata):
        self.loader = loader
        self.result = result
        self.runner = runner
        self.plugins = plugins
        self.connection = connection
        self.excecuteTests = lambda test, result: test(result)
        super(SubprocessEvent, self).__init__(**metadata)


class RegisterInSubprocessEvent(events.Event):
    def __init__(self, **metadata):
        self.pluginClasses = []
        super(RegisterInSubprocessEvent, self).__init__(**metadata)


# custom hook system that records calls and events
class RecordingHook(events.Hook):
    def __init__(self, method, interface):
        super(RecordingHook, self).__init__(method)
        self.interface = interface

    def __call__(self, event):
        res = super(RecordingHook, self).__call__(event)
        self.interface.log(self.method, event)
        return res


class RecordingPluginInterface(events.PluginInterface):
    hookClass = RecordingHook

    def __init__(self):
        super(RecordingPluginInterface, self).__init__()
        self.events = []

    def log(self, method, event):
        self.events.append((method, event))

    def flush(self):
        events = self.events[:]
        self.events = []
        # XXX make pickle safe
        return self._fix(events)

    def _fix(events):
        for event in events:
            if hasattr(event, 'case'):
                event.case = event.case.id()
            if hasattr(event, 'exc_info'):
                ec, ev, tb = event.exc_info
                event.exc_info = (ex, ev, util.format_traceback(tb))
            if hasattr(event, 'result'):
                event.result = None
            if hasattr(event, 'loader'):
                event.loader = None
            if hasattr(event, 'runner'):
                event.runner = None
            yield event

    def __getattr__(self, attr):
        return self.hooks.setdefault(attr, self.hookClass(attr, self))
