"""
This module contains some code copied from unittest2/ and other code
developed in reference to unittest2.

unittest2 is Copyright (c) 2001-2010 Python Software Foundation; All
Rights Reserved. See: http://docs.python.org/license.html

"""
import inspect
import types

from nose2 import util
from nose2.events import Plugin
from nose2.compat import unittest


class Functions(Plugin):
    """TODO: document"""
    configSection = 'functions'

    def __init__(self):
        self.register()

    def loadTestsFromName(self, event):
        name = event.name
        module = event.module
        result = util.test_from_name(name, module)
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
            case = unittest.FunctionTestCase(obj, **args)
            tests.append(case)
        return tests
