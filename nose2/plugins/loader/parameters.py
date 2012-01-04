"""
This module contains some code copied from unittest2 and other code
developed in reference to unittest2.

unittest2 is Copyright (c) 2001-2010 Python Software Foundation; All
Rights Reserved. See: http://docs.python.org/license.html

"""
import logging
import types
import unittest

from nose2 import exceptions, util
from nose2.events import Plugin
from nose2.compat import unittest as ut2

log = logging.getLogger(__name__)


class ParamsFunctionCase(ut2.FunctionTestCase):
    def __init__(self, name, func, **args):
        self._name = name
        ut2.FunctionTestCase.__init__(self, func, **args)

    def __repr__(self):
        return self._name

    id = __str__ = __repr__


class Parameters(Plugin):
    configSection = 'parameters'

    def __init__(self):
        self.register()

    def getTestCaseNames(self, event):
        log.debug('getTestCaseNames %s', event)
        names = filter(event.isTestMethod, dir(event.testCase))
        testCaseClass = event.testCase
        for name in names:
            method = getattr(testCaseClass, name)
            paramList = getattr(method, 'paramList', None)
            if paramList is None:
                continue
            # exclude this method from normal collection
            event.excludedNames.append(name)
            # generate the methods to be loaded by the testcase loader
            self._generate(event, name, method, testCaseClass)

    def loadTestsFromModule(self, event):
        module = event.module
        def is_test(obj):
            return (obj.__name__.startswith(self.session.testMethodPrefix) and
                    hasattr(obj, 'paramList'))
        tests = []
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, types.FunctionType) and is_test(obj):
                tests.extend(
                    self._generateFuncTests(obj)
                    )
        event.extraTests.extend(tests)

    def loadTestsFromName(self, event):
        original_name = name = event.name
        module = event.module
        result = util.test_from_name(name, module)
        if result is None:
            # we can't find it - let the default case handle it
            return

        parent, obj, name, index = result
        if not hasattr(obj, 'paramList'):
            return

        if (index is None
            and not isinstance(parent, type)
            and not isinstance(obj, types.FunctionType)):
            log.debug("Don't know how to load parameterized tests from %s", obj)
            return

        if (parent
            and isinstance(parent, type)
            and issubclass(parent, unittest.TestCase)):
            # generator method
            names = self._generate(event, name, obj, parent)
            tests = [parent(n) for n in names]
        else:
            # generator func
            tests = list(self._generateFuncTests(obj))

        if index is not None:
            try:
                tests = [tests[index-1]]
            except IndexError:
                raise exceptions.TestNotFoundError(original_name)

        suite = event.loader.suiteClass()
        suite.addTests(tests)
        event.handled = True
        return suite

    def _generate(self, event, name, method, testCaseClass):
        names = []
        for index, argSet in enumerate_params(method.paramList):
            method_name = util.name_from_args(name, index, argSet)
            def _method(self, method=method, argSet=argSet):
                return method(self, *argSet)
            if hasattr(testCaseClass, method_name):
                # already generated
                return
            setattr(testCaseClass, method_name, _method)
            names.append(method_name)
        return names

    def _generateFuncTests(self, obj):
        args = {}
        setUp = getattr(obj, 'setUp', None)
        tearDown = getattr(obj, 'tearDown', None)
        if setUp is not None:
            args['setUp'] = setUp
        if tearDown is not None:
            args['tearDown'] = tearDown
        for index, argSet in enumerate_params(obj.paramList):
            def func(argSet=argSet, obj=obj):
                return obj(*argSet)
            name = '%s.%s' % (obj.__module__, obj.__name__)
            func_name = util.name_from_args(name, index, argSet)
            yield ParamsFunctionCase(func_name, func, **args)


def enumerate_params(paramList):
    for index, argSet in enumerate(paramList):
        if not isinstance(argSet, tuple):
            argSet = (argSet,)
        yield index, argSet
