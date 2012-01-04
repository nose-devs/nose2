"""
Adapted from unittest2/events.py from the unittest2 plugins branch.

This module contains some code copied from unittest2/events.py and other
code developed in reference to that module and others within unittest2.

unittest2 is Copyright (c) 2001-2010 Python Software Foundation; All
Rights Reserved. See: http://docs.python.org/license.html

"""
import logging

import argparse
import six

from nose2 import config

log = logging.getLogger(__name__)

# FIXME decide on a real rule for camelCase vs under_score and stick with it.

# XXX I'd rather move this stuff to Plugin.__init__ and
# have __init__ call self.configure() or something after the
# initial setup, but that would further break compatibilty
# with the unittest2 plugins branch Plugin class.
class PluginMeta(type):
    def __call__(cls, *args, **kwargs):
        session = kwargs.pop('session', None)
        instance = object.__new__(cls, *args, **kwargs)
        instance.session = session
        instance.config = config.Config([])

        config_section = getattr(instance, 'configSection', None)
        switch = getattr(instance, 'commandLineSwitch', None)

        if session is not None and config_section is not None:
            instance.config = session.get(config_section)

        always_on = instance.config.as_bool('always-on', default=False)

        instance.__init__(*args, **kwargs)
        if always_on:
            instance.register()
        else:
            if switch is not None:
                short_opt, long_opt, help = switch
                instance.addOption(
                    instance.register, short_opt, long_opt, help)
        return instance


class Plugin(six.with_metaclass(PluginMeta)):

    def register(self, *_):
        """Add myself to the plugins that get called"""
        if self.session is None:
            log.warning("Unable to register %s, no session", self)
            return
        self.session.registerPlugin(self)

    def addFlag(self, callback, short_opt, long_opt, help_text=None):
        self.addOption(callback, short_opt, long_opt, help_text, nargs=0)

    def addArgument(self, callback, short_opt, long_opt, help_text=None):
        self.addOption(callback, short_opt, long_opt, help_text, nargs=1)

    def addOption(self, callback, short_opt, long_opt, help_text=None, nargs=0):
        """Add command-line option"""
        if self.session is None:
            log.warning("Unable to add option %s/%s for %s, no session",
                        short_opt, long_opt, self)
            return
        class CB(argparse.Action):
            def __call__(self, parser, namespace, values, option_string=None):
                if six.callable(callback):
                    callback(values)
                elif isinstance(callback, list):
                    callback.append(values)
                else:
                    raise ValueError("Invalid callback %s for plugin option %s",
                                     callback, option_string)
        opts = []
        if short_opt:
            if short_opt.lower() == short_opt:
                raise ValueError(
                    'Lowercase short options are reserved: %s' % short_opt)
            opts.append('-' + short_opt)
        if long_opt:
            opts.append('--' + long_opt)
        self.session.argparse.add_argument(
            *opts, action=CB, help=help_text, const=True, nargs=nargs)


class Hook(object):
    def __init__(self, method):
        self.method = method
        self.plugins = []

    def __call__(self, event):
        for plugin in self.plugins[:]:
            result = getattr(plugin, self.method)(event)
            if event.handled:
                return result

    def append(self, plugin):
        self.plugins.append(plugin)


class PluginInterface(object):
    methods = ('pluginsLoaded', 'loadTestsFromModule', 'loadTestsFromNames',
               'handleFile', 'startTestRun', 'startTest', 'stopTest',
               'loadTestsFromName', 'loadTestsFromTestCase',
               'stopTestRun', 'matchPath', 'getTestCaseNames',
               'runnerCreated', 'resultCreated', 'testOutcome', 'wasSuccessful',
               'resultStop', 'setTestOutcome', 'describeTest',
               'reportStartTest', 'reportError', 'reportFailure', 'reportSkip',
               'reportSuccess', 'reportExpectedFailure', 'reportUnexpectedSuccess',
               'reportOtherOutcome', 'outcomeDetail', 'beforeErrorList',
               'beforeSummary', 'afterSummary',
               # ... etc
               )

    def __init__(self):
        self.hooks = {}

    def addMethod(self, method):
        self.methods = self.methods + (method,)

    def register(self, method, plugin):
        self.hooks.setdefault(method, Hook(method)).append(plugin)

    def __getattr__(self, attr):
        return self.hooks.setdefault(attr, Hook(attr))


class Event(object):
    def __init__(self):
        self.handled = False
        self.metadata = {}

    def message(self, message, verbosity=(1, 2)):
        raise NotImplementedError("Not supported")


class PluginsLoadedEvent(Event):
    def __init__(self, pluginsLoaded, **kw):
        self.pluginsLoaded = pluginsLoaded
        super(PluginsLoadedEvent, self).__init__(**kw)


class RunnerCreatedEvent(Event):
    def __init__(self, runner, **kw):
        self.runner = runner
        super(RunnerCreatedEvent, self).__init__(**kw)


class ResultCreatedEvent(Event):
    def __init__(self, result, **kw):
        self.result = result
        super(ResultCreatedEvent, self).__init__(**kw)


class StartTestRunEvent(Event):
    def __init__(self, runner, suite, result, startTime, executeTests, **kw):
        self.suite = suite
        self.runner = runner
        self.result = result
        self.startTime = startTime
        self.executeTests = executeTests
        super(StartTestRunEvent, self).__init__(**kw)


class StopTestRunEvent(Event):
    def __init__(self, runner, result, stopTime, timeTaken, **kw):
        self.runner = runner
        self.result = result
        self.stopTime = stopTime
        self.timeTaken = timeTaken
        super(StopTestRunEvent, self).__init__(**kw)


class StartTestEvent(Event):
    def __init__(self, test, result, startTime, **kw):
        self.test = test
        self.result = result
        self.startTime = startTime
        super(StartTestEvent, self).__init__(**kw)


class StopTestEvent(Event):
    def __init__(self, test, result, stopTime, **kw):
        self.test = test
        self.result = result
        self.stopTime = stopTime
        super(StopTestEvent, self).__init__(**kw)


class TestOutcomeEvent(Event):
    def __init__(self, test, result, outcome, exc_info=None, reason=None,
                 expected=True, shortLabel=None, longLabel=None, **kw):
        self.test = test
        self.result = result
        self.outcome = outcome
        self.exc_info = exc_info
        self.reason = reason
        self.expected = expected
        self.shortLabel = shortLabel
        self.longLabel = longLabel
        super(TestOutcomeEvent, self).__init__(**kw)


class LoadFromModuleEvent(Event):
    def __init__(self, loader, module, useLoadTests=False, **kw):
        self.loader = loader
        self.module = module
        self.useLoadTests = useLoadTests
        self.extraTests = []
        super(LoadFromModuleEvent, self).__init__(**kw)


class LoadFromTestCaseEvent(Event):
    def __init__(self, loader, testCase, **kw):
        self.loader = loader
        self.testCase = testCase
        self.extraTests = []
        super(LoadFromTestCaseEvent, self).__init__(**kw)


class LoadFromNamesEvent(Event):
    def __init__(self, loader, names, module, **kw):
        self.loader = loader
        self.names = names
        self.module = module
        self.extraTests = []
        super(LoadFromNamesEvent, self).__init__(**kw)

    def __str__(self):
        return "LoadFromNames(names=%r, module=%r)" % (self.names, self.module)


class LoadFromNameEvent(Event):
    def __init__(self, loader, name, module, **kw):
        self.loader = loader
        self.name = name
        self.module = module
        self.extraTests = []
        super(LoadFromNameEvent, self).__init__(**kw)



class HandleFileEvent(Event):
    def __init__(self, loader, name, path, pattern, topLevelDirectory, **kw):
        self.extraTests = []
        self.path = path
        self.loader = loader
        self.name = name
        # note: pattern may be None if not called during test discovery
        self.pattern = pattern
        self.topLevelDirectory = topLevelDirectory
        super(HandleFileEvent, self).__init__(**kw)


class MatchPathEvent(Event):
    def __init__(self, name, path, pattern, **kw):
        self.path = path
        self.name = name
        self.pattern = pattern
        super(MatchPathEvent, self).__init__(**kw)


class GetTestCaseNamesEvent(Event):
    def __init__(self, loader, testCase, isTestMethod, **kw):
        self.loader = loader
        self.testCase = testCase
        self.testMethodPrefix = None
        self.extraNames = []
        self.excludedNames = []
        self.isTestMethod = isTestMethod
        super(GetTestCaseNamesEvent, self).__init__(**kw)


class ResultSuccessEvent(Event):
    def __init__(self, result, success, **kw):
        self.result = result
        self.success = success
        super(ResultSuccessEvent, self).__init__(**kw)


class ResultStopEvent(Event):
    def __init__(self, result, shouldStop, **kw):
        self.result = result
        self.shouldStop = shouldStop
        super(ResultStopEvent, self).__init__(**kw)


class DescribeTestEvent(Event):
    def __init__(self, test, description=None, **kw):
        self.test = test
        self.description = description
        super(DescribeTestEvent, self).__init__(**kw)


class OutcomeDetailEvent(Event):
    def __init__(self, outcomeEvent, **kw):
        self.outcomeEvent = outcomeEvent
        self.extraDetail = []
        super(OutcomeDetailEvent, self).__init__(**kw)


class ReportSummaryEvent(Event):
    def __init__(self, stopTestEvent, stream, reportCategories, **kw):
        self.stopTestEvent = stopTestEvent
        self.stream = stream
        self.reportCategories = reportCategories
        super(ReportSummaryEvent, self).__init__(**kw)


class ReportTestEvent(Event):
    def __init__(self, testEvent, stream, **kw):
        self.testEvent = testEvent
        self.stream = stream
        super(ReportTestEvent, self).__init__(**kw)
