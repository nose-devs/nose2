import logging
import multiprocessing
import select
import unittest

import six

from nose2 import events, loader, result, runner, session, util

log = logging.getLogger(__name__)


class MultiProcess(events.Plugin):
    configSection = 'multiprocess'

    def __init__(self):
        self.addArgument(self.setProcs, 'N', '--processes', '# o procs')
        self.testRunTimeout = self.config.as_float('test-run-timeout', 60.0)
        self.procs = self.config.as_int('processes', multiprocessing.cpu_count())
        self.cases = {}

    def setProcs(self, num):
        self.procs = int(num[0]) # FIXME merge n fix
        self.register()

    def pluginsLoaded(self, event):
        self.addMethods('registerInSubprocess', 'startSubprocess',
                        'stopSubprocess')

    def startTestRun(self, event):
        event.executeTests = self._runmp

    def beforeInteraction(self, event):
        # prevent interactive plugins from running
        event.handled = True
        return False

    def _runmp(self, test, result):
        flat = list(self._flatten(test))
        procs = self._startProcs()

        # distribute tests more-or-less evenly among processes
        while flat:
            for proc, conn in procs:
                if not flat:
                    break
                caseid = flat.pop(0)
                conn.send(caseid)

        # None is the 'done' flag
        for proc, conn in procs:
            conn.send(None)

        # wait for results
        procs = [(p,c) for p, c in procs if p.is_alive()]
        rdrs = [conn for proc, conn in procs
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
                    rdrs.remove(conn)
                    continue # XXX or die?

                if remote_events is None:
                    # XXX proc is done, how to mark it dead?
                    rdrs.remove(conn)
                    continue
                # replay events
                testid, events = remote_events
                log.debug("Received results for %s", testid)
                for (hook, event) in events:
                    log.debug("Received %s(%s)", hook, event)
                    self._localize(event)
                    getattr(self.session.hooks, hook)(event)
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
        # examine suite tests to find out if they have class
        # or module fixtures and group them that way into names
        # of test classes or modules
        # ALSO record all test cases in self.cases
        mods = {}
        classes = {}
        stack = [suite]
        while stack:
            suite = stack.pop()
            for test in suite:
                if isinstance(test, unittest.TestSuite):
                    stack.append(test)
                else:
                    testid = util.test_name(test)
                    self.cases[testid] = test
                    if util.has_module_fixtures(test):
                        mods.setdefault(test.__class__.__module__, []).append(
                            testid)
                    elif util.has_class_fixtures(test):
                        classes.setdefault("%s.%s" % (test.__class__.__module__,
                                                      test.__class__.__name__),
                                           []).append(testid)
                    else:
                        yield testid
        for cls in classes.keys():
            yield cls
        for mod in mods.keys():
            yield mod

    def _localize(self, event):
        # XXX set loader, case, result etc to local ones, if present in event
        # (event case will be just the id)
        # (traceback in exc_info if any won't be real!)
        if hasattr(event, 'result'):
            event.result = self.session.testResult
        if hasattr(event, 'loader'):
            event.loader = self.session.testLoader
        if hasattr(event, 'runner'):
            event.runner = self.session.testRunner
        if hasattr(event, 'test') and isinstance(event.test, six.string_types):
            # remote event.case is the test id
            try:
                event.test = self.cases[event.test]
            except KeyError:
                event.test = self.session.testLoader.failedLoadTests(
                    'test_not_found',
                    RuntimeError("Unable to locate test case for %s in "
                                 "main process" % event.test))._tests[0]

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
    # init logging system
    rlog = multiprocessing.log_to_stderr()
    rlog.setLevel(session_export['logLevel'])

    # make a real session from the "session" we got
    ssn = session.Session()
    ssn.config = session_export['config']
    ssn.hooks = RecordingPluginInterface()
    ssn.verbosity = session_export['verbosity']
    ssn.startDir = session_export['startDir']
    ssn.topLevelDir = session_export['topLevelDir']
    ssn.prepareSysPath()
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
        conn.send(None)
        conn.close()
        ssn.hooks.stopSubprocess(event)
        return
    # receive and run tests
    executor = event.executeTests
    for testid in gentests(conn):
        if testid is None:
            break
        test = event.loader.loadTestsFromName(testid)
        # xxx try/except?
        rlog.debug("Execute test %s (%s)", testid, test)
        executor(test, event.result)
        events = [e for e in ssn.hooks.flush()]
        conn.send((testid, events))
        rlog.debug("Log for %s returned", testid)
    conn.send(None)
    conn.close()
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
    """Event fired at start and end of subprocess execution.

    .. attribute :: loader

       Test loader instance

    .. attribute :: result

       Test result

    .. attribute :: plugins

       List of plugins loaded in the subprocess.

    .. attribute :: connection

       The :class:`multiprocessing.Connection` instance that the
       subprocess uses for communication with the main process.

    .. attribute :: executeTests

       Callable that will be used to execute tests.  Plugins may set
       this attribute to wrap or otherwise change test execution. The
       callable must match the signature::

         def execute(suite, result):
             ...

    """
    def __init__(self, loader, result, runner, plugins, connection, **metadata):
        self.loader = loader
        self.result = result
        self.runner = runner
        self.plugins = plugins
        self.connection = connection
        self.executeTests = lambda test, result: test(result)
        super(SubprocessEvent, self).__init__(**metadata)


class RegisterInSubprocessEvent(events.Event):
    """Event fired to notify plugins that multiprocess testing will occur

    .. attribute :: pluginClasses

       Add a plugin class to this list to cause the plugin to be
       instantiated in each test-running subprocess. The most common
       thing to do, for plugins that need to run in subprocesses, is::

         def registerInSubprocess(self, event):
             event.pluginClasses.append(self.__class__)

    """
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
    noLogMethods = set(['getTestCaseNames', 'startSubprocess', 'stopSubprocess',
                        'registerInSubprocess'])

    def __init__(self):
        super(RecordingPluginInterface, self).__init__()
        self.events = []

    def log(self, method, event):
        self.events.append((method, event))

    def flush(self):
        events = self.events[:]
        self.events = []
        return events

    def register(self, method, plugin):
        """Register a plugin for a method.

        :param method: A method name
        :param plugin: A plugin instance

        """
        self._hookForMethod(method).append(plugin)

    def __getattr__(self, attr):
        if attr.startswith('__'):
            raise AttributeError('No %s in %s' % (attr, self))
        return self._hookForMethod(attr)

    def _hookForMethod(self, method):
        # return recording hook for most hooks, normal hook for those
        # (like test loading and subprocess events) that we don't want
        # to send back to the main process.
        try:
            return self.hooks[method]
        except KeyError:
            if method in self.noLogMethods or method.startswith('loadTest'):
                hook = events.Hook(method)
            else:
                hook = self.hookClass(method, self)
        self.hooks[method] = hook
        return hook

