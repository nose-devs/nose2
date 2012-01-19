"""
Load tests from :class:`unittest.TestCase` subclasses.

This plugin implements :func:`loadTestsFromName` and
:func:`loadTestsFromModule` to load tests from
:class:`unittest.TestCase` subclasses found in modules or named on the
command line.


"""
# Adapted from unittest2/loader.py from the unittest2 plugins branch.
# This module contains some code copied from unittest2/loader.py and other
# code developed in reference to that module and others within unittest2.
# unittest2 is Copyright (c) 2001-2010 Python Software Foundation; All
# Rights Reserved. See: http://docs.python.org/license.html

import unittest

from nose2 import events, util


__unittest = True


class TestCaseLoader(events.Plugin):
    """Loader plugin that loads from test cases"""
    alwaysOn = True
    configSection = 'testcases'

    def loadTestsFromModule(self, event):
        """Load tests in :class:`unittest.TestCase` subclasses"""
        module = event.module
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, unittest.TestCase):
                event.extraTests.append(self._loadTestsFromTestCase(event, obj))

    def loadTestsFromName(self, event):
        """Load tests from event.name if it names a test case/method"""
        name = event.name
        module = event.module
        result = util.test_from_name(name, module)
        if result is None:
            return
        parent, obj, name, index = result
        if isinstance(obj, type) and issubclass(obj, unittest.TestCase):
            # name is a test case class
            event.extraTests.append(self._loadTestsFromTestCase(event, obj))
        elif (isinstance(parent, type) and
              issubclass(parent, unittest.TestCase) and not
              util.isgenerator(obj) and not
              hasattr(obj, 'paramList')):
            # name is a single test method
            event.extraTests.append(parent(obj.__name__))

    def _loadTestsFromTestCase(self, event, testCaseClass):
        evt = events.LoadFromTestCaseEvent(event.loader, testCaseClass)
        result = self.session.hooks.loadTestsFromTestCase(evt)
        if evt.handled:
            loaded_suite = result or event.loader.suiteClass()
        else:
            names = self._getTestCaseNames(event, testCaseClass)
            if not names and hasattr(testCaseClass, 'runTest'):
                names = ['runTest']
            # FIXME return failure test case if name not in testcase class
            loaded_suite = event.loader.suiteClass(map(testCaseClass, names))
        if evt.extraTests:
            loaded_suite.addTests(evt.extraTests)
        return loaded_suite

    def _getTestCaseNames(self, event, testCaseClass):
        excluded = set()
        def isTestMethod(attrname, testCaseClass=testCaseClass,
                         excluded=excluded):
            prefix = evt.testMethodPrefix or self.session.testMethodPrefix
            return (
                attrname.startswith(prefix) and
                hasattr(getattr(testCaseClass, attrname), '__call__') and
                attrname not in excluded
            )
        evt = events.GetTestCaseNamesEvent(
            event.loader, testCaseClass, isTestMethod)
        result = self.session.hooks.getTestCaseNames(evt)
        if evt.handled:
            test_names = result or []
        else:
            excluded.update(evt.excludedNames)
            test_names = [entry for entry in dir(testCaseClass)
                          if isTestMethod(entry)]
        if evt.extraNames:
            test_names.extend(evt.extraNames)
        if event.loader.sortTestMethodsUsing:
            test_names.sort(
                key=event.loader.sortTestMethodsUsing)
        return test_names
