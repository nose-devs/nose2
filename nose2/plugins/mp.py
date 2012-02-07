import logging
import multiprocessing
import select
import unittest

from nose2 import events, loader, result, runner, session

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
    def pluginsLoaded(self, event):
        self.session.hooks.addMethod('registerInSubprocess')
        self.session.hooks.addMethod('startSubprocess')
        self.session.hooks.addMethod('stopSubprocess')
        for plugin in event.pluginsLoaded:
            if plugin.registered and hasattr(plugin, 'registerInSubprocess'):
                self.session.hooks.register('registerInSubprocess', plugin)

    def startTestRun(self, event):
        event.executeTests = self._runmp

    def _runmp(self, test, result):
        self.cases = {}
        flat = self._flatten(test)
        procs = self._startProcs()

        # distribute tests more-or-less evenly among processes
        while flat:
            for proc, conn in procs:
                if not flat:
                    break
                caseid = flat.pop(0)
                print "))) %s ---> %s" % (caseid, proc)
                conn.send(caseid)

        # None is the 'done' flag
        for proc, conn in procs:
            conn.send(None)

        # wait for results
        procs = [(p,c) for p, c in procs if p.is_alive()]
        rdrs = [conn for proc, conn in procs
                if proc.is_alive()]
        while rdrs:
            print "+++", rdrs
            # FIXME landing here w/dead connections, then
            # sitting until testRunTimeout. need to detect
            # earlier that proc conns are dead
            ready, _, _ = select.select(rdrs, [], [], self.testRunTimeout)
            for conn in ready:
                # XXX proc could be dead
                try:
                    remote_events = conn.recv()
                except EOFError:
                    # probably dead
                    log.warning("Subprocess connection closed unexpectedly")
                    continue # XXX or die?
                print ">>>>>>>>>>>>>>>", remote_events
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
        # really: examine suite tests to find out if they have class
        # or module fixtures and group them that way into names
        # of test classes or modules
        # ALSO record all test cases in self._cases
        flat = []
        for test in suite:
            if isinstance(test, unittest.TestSuite):
                flat.extend(self._flatten(test))
            else:
                # XXX does not work for test funcs
                testid = test.id()
                if '\n' in testid:
                    testid = testid.split('\n')[0] # FIXME refactor
                flat.append(testid)
                self.cases[testid] = test
        print "******", len(flat)
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
        if hasattr(event, 'test') and event.test in self.cases:
            # remote event.case is the test id
            event.test = self.cases[event.test]
        elif isinstance(event.test, basestring):
            import pdb; pdb.set_trace()

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
    ssn.hooks = RecordingPluginInterface()
    ssn.verbosity = session_export['verbosity']
    ssn.startDir = session_export['startDir']
    ssn.topLevelDir = session_export['topLevelDir']

    # init logging system
    logging.basicConfig(level=logging.DEBUG) # level=session_export['logLevel'])
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
        events = [e for e in ssn.hooks.flush()]
        print conn
        print testid
        print events
        conn.send((testid, events))
        rlog.debug("Log for %s returned", testid)
    conn.send(None)
    conn.close()
    ssn.hooks.stopSubprocess(event)
    print "***** FINISHED! *****"


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
        self.executeTests = lambda test, result: test(result)
        self.nolog = True
        super(SubprocessEvent, self).__init__(**metadata)


class RegisterInSubprocessEvent(events.Event):
    def __init__(self, **metadata):
        self.pluginClasses = []
        self.nolog = True
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
        print "log called", method, event
        if getattr(event, 'nolog', False):
            return
        if method.startswith('loadTest'):
            # do not want to replay loading
            return
        self.events.append((method, event))

    def flush(self):
        print "flush called"
        events = self.events[:]
        self.events = []
        # XXX make pickle safe?
        return events

    def _fix(self, events):
        return events
        # for method, event in events:
        #     newevent = event.copy()
        #     if hasattr(event, 'case'):
        #         newevent.case = event.case.id()
        #     if hasattr(event, 'exc_info'):
        #         ec, ev, tb = event.exc_info
        #         newevent.exc_info = (ec, ev, util.format_traceback(tb))
        #     if hasattr(event, 'result'):
        #         newevent.result = None
        #     if hasattr(event, 'loader'):
        #         newevent.loader = None
        #     if hasattr(event, 'runner'):
        #         newevent.runner = None
        #     for attr in dir(event):
        #         item = getattr(event, attr)
        #         if isinstance(item, types.FunctionType):
        #             setattr(newevent, attr, None)
        #     yield (method, newevent)

    def register(self, method, plugin):
        """Register a plugin for a method.

        :param method: A method name
        :param plugin: A plugin instance

        """
        self.hooks.setdefault(
            method, self.hookClass(method, self)).append(plugin)

    def __getattr__(self, attr):
        print "getattr", attr
        if attr.startswith('__'):
            raise AttributeError('No %s in %s' % (attr, self))
        return self.hooks.setdefault(attr, self.hookClass(attr, self))
