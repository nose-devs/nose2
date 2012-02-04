"""
Load tests from test functions in modules.

This plugin responds to :func:`loadTestsFromModule` by adding test
cases for all test functions in the module to ``event.extraTests``. It
uses ``session.testMethodPrefix`` to find test functions.

Functions that are generators, have param lists, or take arguments
are not collected.

This plugin also implements :func:`loadTestsFromName` to enable loading
tests from dotted function names passed on the command line.

"""
# This module contains some code copied from unittest2/ and other code
# developed in reference to unittest2.
# unittest2 is Copyright (c) 2001-2010 Python Software Foundation; All
# Rights Reserved. See: http://docs.python.org/license.html


import inspect
import types

from nose2 import util
from nose2.events import Plugin
from nose2.compat import unittest


__unittest = True


class Functions(Plugin):
    """Loader plugin that loads test functions"""
    alwaysOn = True
    configSection = 'functions'

    def loadTestsFromName(self, event):
        """Load test if event.name is the name of a test function"""
        name = event.name
        module = event.module
        try:
            result = util.test_from_name(name, module)
        except (AttributeError, ImportError) as e:
            event.handled = True
            return event.loader.failedLoadTests(name, e)
        if result is None:
            return

        parent, obj, name, index = result
        if (isinstance(obj, types.FunctionType) and not
            util.isgenerator(obj) and not
            hasattr(obj, 'paramList') and not
            inspect.getargspec(obj).args):
            suite = event.loader.suiteClass()
            suite.addTests(self._createTests(obj))
            event.handled = True
            return suite

    def loadTestsFromModule(self, event):
        """Load test functions from event.module"""
        module = event.module

        def is_test(obj):
            if not obj.__name__.startswith(self.session.testMethodPrefix):
                return False
            if inspect.getargspec(obj).args:
                return False
            return True

        tests = []
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, types.FunctionType) and is_test(obj):
                tests.extend(self._createTests(obj))
        event.extraTests.extend(tests)

    def _createTests(self, obj):
        if not hasattr(obj, 'setUp'):
            if hasattr(obj, 'setup'):
                obj.setUp = obj.setup
            elif hasattr(obj, 'setUpFunc'):
                obj.setUp = obj.setUpFunc
        if not hasattr(obj, 'tearDown'):
            if hasattr(obj, 'teardown'):
                obj.tearDown = obj.teardowns
            elif hasattr(obj, 'tearDownFunc'):
                obj.tearDown = obj.tearDownFunc

        tests = []
        args = {}
        setUp = getattr(obj, 'setUp', None)
        tearDown = getattr(obj, 'tearDown', None)
        if setUp is not None:
            args['setUp'] = setUp
        if tearDown is not None:
            args['tearDown'] = tearDown

        paramList = getattr(obj, 'paramList', None)
        isGenerator = util.isgenerator(obj)
        if paramList is not None or isGenerator:
            return tests
        else:
            case = util.transplant_class(
                unittest.FunctionTestCase, obj.__module__)(obj, **args)
            tests.append(case)
        return tests
