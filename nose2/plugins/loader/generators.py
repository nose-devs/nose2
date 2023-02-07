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
append a colon (':') followed by the index (*starting from 1*) of the
generated case you want to execute.

"""
# This module contains some code copied from unittest2 and other code
# developed in reference to unittest2.
# unittest2 is Copyright (c) 2001-2010 Python Software Foundation; All
# Rights Reserved. See: http://docs.python.org/license.html

import functools
import inspect
import logging
import sys
import types
import unittest

from nose2 import exceptions, util
from nose2.events import Plugin

log = logging.getLogger(__name__)
__unittest = True


class Generators(Plugin):

    """Loader plugin that loads generator tests"""

    alwaysOn = True
    configSection = "generators"

    def registerInSubprocess(self, event):
        event.pluginClasses.append(self.__class__)

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
        log.debug("loadTestsFromTestCase %s", event.testCase)
        testCaseClass = event.testCase
        for name, method in util.iter_attrs(testCaseClass):
            if not inspect.isgeneratorfunction(method):
                continue
            if not name.startswith(self.session.testMethodPrefix):
                continue
            instance = testCaseClass(name)
            event.extraTests.extend(
                self._testsFromGenerator(event, name, method(instance), testCaseClass)
            )

    def loadTestsFromTestClass(self, event):
        testCaseClass = event.testCase
        for name, method in util.iter_attrs(testCaseClass):
            if not inspect.isgeneratorfunction(method):
                continue
            if not name.startswith(self.session.testMethodPrefix):
                continue
            instance = testCaseClass()
            event.extraTests.extend(
                self._testsFromGeneratorMethod(event, name, method, instance)
            )

    def getTestCaseNames(self, event):
        """Get generator test case names from test case class"""
        log.debug("getTestCaseNames %s", event.testCase)
        for name, method in util.iter_attrs(event.testCase):
            if not inspect.isgeneratorfunction(method):
                continue
            if not event.isTestMethod(name):
                continue
            event.excludedNames.append(name)

    def getTestMethodNames(self, event):
        return self.getTestCaseNames(event)

    def loadTestsFromName(self, event):
        """Load tests from generator named on command line"""
        original_name = name = event.name
        module = event.module
        try:
            result = util.test_from_name(name, module)
        except (AttributeError, ImportError):
            event.handled = True
            return event.loader.failedLoadTests(name, sys.exc_info())
        if result is None:
            # we can't find it - let the default case handle it
            return

        parent, obj, name, index = result
        if not inspect.isgeneratorfunction(obj):
            return

        if (
            index is None
            and not isinstance(parent, type)
            and not isinstance(obj, types.FunctionType)
        ):
            log.debug("Don't know how to load generator tests from %s", obj)
            return

        if (
            parent
            and isinstance(parent, type)
            and issubclass(parent, unittest.TestCase)
        ):
            # generator method in test case
            instance = parent(obj.__name__)
            tests = list(
                self._testsFromGenerator(event, obj.__name__, obj(instance), parent)
            )
        elif parent and isinstance(parent, type):
            # generator method in test class
            method = obj
            instance = parent()
            tests = list(self._testsFromGeneratorMethod(event, name, method, instance))
        else:
            # generator func
            tests = list(self._testsFromGeneratorFunc(event, obj))

        if index is not None:
            try:
                tests = [tests[index - 1]]
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
            return obj.__name__.startswith(
                self.session.testMethodPrefix
            ) and inspect.isgeneratorfunction(obj)

        tests = []
        for _, obj in util.iter_attrs(module):
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
        except Exception as e:
            test_name = "{}.{}.{}".format(
                testCaseClass.__module__,
                testCaseClass.__name__,
                name,
            )
            yield event.loader.failedLoadTests(test_name, e)

    def _testsFromGeneratorFunc(self, event, obj):
        extras = list(obj())
        name = f"{obj.__module__}.{obj.__name__}"
        args = {}
        setUp = getattr(obj, "setUp", None)
        tearDown = getattr(obj, "tearDown", None)
        if setUp is not None:
            args["setUp"] = setUp
        if tearDown is not None:
            args["tearDown"] = tearDown

        def createTest(name):
            return util.transplant_class(GeneratorFunctionCase, obj.__module__)(
                name, **args
            )

        yield from self._testsFromGenerator(event, name, extras, createTest)

    def _testsFromGeneratorMethod(self, event, name, method, instance):
        extras = list(method(instance))
        name = "{}.{}.{}".format(
            instance.__class__.__module__,
            instance.__class__.__name__,
            method.__name__,
        )
        args = {}
        setUp = getattr(instance, "setUp", None)
        tearDown = getattr(instance, "tearDown", None)
        if setUp is not None:
            args["setUp"] = setUp
        if tearDown is not None:
            args["tearDown"] = tearDown

        def createTest(name):
            return util.transplant_class(
                GeneratorMethodCase(instance.__class__), instance.__class__.__module__
            )(name, **args)

        yield from self._testsFromGenerator(event, name, extras, createTest)


class GeneratorFunctionCase(unittest.FunctionTestCase):
    def __init__(self, name, **args):
        self._funcName = name
        unittest.FunctionTestCase.__init__(self, None, **args)

    _testFunc = property(
        lambda self: getattr(self, self._funcName), lambda self, func: None
    )

    def __repr__(self):
        return self._funcName

    id = __str__ = __repr__


def GeneratorMethodCase(cls):
    class _GeneratorMethodCase(GeneratorFunctionCase):
        if util.has_class_fixtures(cls):

            @classmethod
            def setUpClass(klass):
                if hasattr(cls, "setUpClass"):
                    cls.setUpClass()

            @classmethod
            def tearDownClass(klass):
                if hasattr(cls, "tearDownClass"):
                    cls.tearDownClass()

    # XXX retain original class name
    _GeneratorMethodCase.__name__ = cls.__name__
    return _GeneratorMethodCase
