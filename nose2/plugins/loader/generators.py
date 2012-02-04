"""
Load tests from generators.

This plugin implements :func:`loadTestFromTestCase`,
:func:`loadTestsFromName` and :func:`loadTestFromModule` to enable
loading tests from generators.

Generators may be functions or methods in test cases. In either case,
they must yield a callable and arguments for that callable once for
each test they generate. The callable and arguments may all be in one
tuple, or the arguments may be grouped into a separate tuple::

  def test_gen():
      yield check, 1, 2
      yield check, (1, 2)

To address a particular generated test via a command-line test name,
append a colon (':') followed by the index, *starting from 1*, of the
generated case you want to execute.

"""
# This module contains some code copied from unittest2 and other code
# developed in reference to unittest2.
# unittest2 is Copyright (c) 2001-2010 Python Software Foundation; All
# Rights Reserved. See: http://docs.python.org/license.html

import functools
import logging
import sys
import types
import unittest

from nose2 import exceptions, util
from nose2.events import Plugin
from nose2.compat import unittest as ut2


log = logging.getLogger(__name__)
__unittest = True


class Generators(Plugin):
    """Loader plugin that loads generator tests"""
    alwaysOn = True
    configSection = 'generators'

    def unpack(self, generator):
        for index, func_args in enumerate(generator):
            try:
                func, args = func_args
                if not isinstance(args, tuple):
                    args = (args,)
                yield index, (func, args)
            except ValueError:
                func, args = func_args[0], func_args[1:]
                yield index, (func, args)

    def loadTestsFromTestCase(self, event):
        """Load generator tests from test case"""
        log.debug('loadTestsFromTestCase %s', event.testCase)
        testCaseClass = event.testCase
        for name in dir(testCaseClass):
            method = getattr(testCaseClass, name)
            if (name.startswith(self.session.testMethodPrefix) and
                hasattr(getattr(testCaseClass, name), '__call__') and
                util.isgenerator(method)):
                instance = testCaseClass(name)
                event.extraTests.extend(
                    self._testsFromGenerator(
                        event, name, method(instance), testCaseClass)
                )

    def getTestCaseNames(self, event):
        """Get generator test case names from test case class"""
        log.debug('getTestCaseNames %s', event.testCase)
        names = filter(event.isTestMethod, dir(event.testCase))
        klass = event.testCase
        for name in names:
            method = getattr(klass, name)
            if util.isgenerator(method):
                event.excludedNames.append(name)

    def loadTestsFromName(self, event):
        """Load tests from generator named on command line"""
        original_name = name = event.name
        module = event.module
        try:
            result = util.test_from_name(name, module)
        except (AttributeError, ImportError) as e:
            event.handled = True
            return event.loader.failedLoadTests(name, e)
        if result is None:
            # we can't find it - let the default case handle it
            return

        parent, obj, name, index = result
        if not util.isgenerator(obj):
            return

        if (index is None
            and not isinstance(parent, type)
            and not isinstance(obj, types.FunctionType)):
            log.debug("Don't know how to load generator tests from %s", obj)
            return

        if (parent
            and isinstance(parent, type)
            and issubclass(parent, unittest.TestCase)):
            # generator method
            instance = parent(obj.__name__)
            tests = list(
                self._testsFromGenerator(event, name, obj(instance), parent)
                    )
        else:
            # generator func
            tests = list(self._testsFromGeneratorFunc(event, obj))

        if index is not None:
            try:
                tests = [tests[index-1]]
            except IndexError:
                raise exceptions.TestNotFoundError(original_name)

        suite = event.loader.suiteClass()
        suite.addTests(tests)
        event.handled = True
        return suite

    def loadTestsFromModule(self, event):
        """Load tests from generator functions in a module"""
        module = event.module

        def is_test(obj):
            return (obj.__name__.startswith(self.session.testMethodPrefix)
                    and util.isgenerator(obj))
        tests = []
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, types.FunctionType) and is_test(obj):
                tests.extend(self._testsFromGeneratorFunc(event, obj))
        event.extraTests.extend(tests)

    def _testsFromGenerator(self, event, name, generator, testCaseClass):
        try:
            for index, (func, args) in self.unpack(generator):
                method_name = util.name_from_args(name, index, args)
                setattr(testCaseClass, method_name, None)
                instance = testCaseClass(method_name)
                delattr(testCaseClass, method_name)
                def method(func=func, args=args):
                    return func(*args)
                method = functools.update_wrapper(method, func)
                setattr(instance, method_name, method)
                yield instance
        except:
            exc_info = sys.exc_info()
            test_name = '%s.%s.%s' % (testCaseClass.__module__,
                                      testCaseClass.__name__,
                                      name)
            yield event.loader.failedLoadTests(test_name, exc_info)

    def _testsFromGeneratorFunc(self, event, obj):
        extras = list(obj())
        name = '%s.%s' % (obj.__module__, obj.__name__)
        args = {}
        setUp = getattr(obj, 'setUp', None)
        tearDown = getattr(obj, 'tearDown', None)
        if setUp is not None:
            args['setUp'] = setUp
        if tearDown is not None:
            args['tearDown'] = tearDown
        def createTest(name):
            return util.transplant_class(
                GeneratorFunctionCase, obj.__module__)(name, **args)
        for test in self._testsFromGenerator(event, name, extras, createTest):
            yield test


class GeneratorFunctionCase(ut2.FunctionTestCase):
    def __init__(self, name, **args):
        self._name = name
        ut2.FunctionTestCase.__init__(self, None, **args)

    _testFunc = property(lambda self: getattr(self, self._name),
                         lambda self, func: None)

    def __repr__(self):
        return self._name

    id = __str__ = __repr__
