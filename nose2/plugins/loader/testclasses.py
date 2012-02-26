import unittest

from nose2 import events, util
from nose2.compat import unittest as ut2

__unittest = True


class TestClasses(events.Plugin):
    alwaysOn = True
    configSection = 'test-classes'

    def loadTestsFromModule(self, event):
        module = event.module
        for name in dir(module):
            obj = getattr(module, name)
            if (isinstance(obj, type) and
                not isinstance(obj, (unittest.TestCase, unittest.TestSuite)) and
                name.lower().startswith(self.session.testMethodPrefix)):
                event.extraTests.append(
                    self._loadTestsFromTestClass(event, obj))


    def _loadTestsFromTestClass(self, event, cls):
        # ... fire event for others to load from
        names = self._getTestMethodNames(event, cls)
        loaded_suite = event.loader.suiteClass(
            [util.transplant_class(MethodTestCase, cls.__module__)(cls, name)
             for name in names])
        # ... add extra tests
        return loaded_suite

    def _getTestMethodNames(self, event, cls):
        # ... give others a chance to modify list
        excluded = set()
        def isTestMethod(attrname, cls=cls, excluded=excluded):
            # FIXME allow plugs to change prefix
            prefix = self.session.testMethodPrefix
            return (
                attrname.startswith(prefix) and
                hasattr(getattr(cls, attrname), '__call__') and
                attrname not in excluded
                )
        test_names = [entry for entry in dir(cls)
                      if isTestMethod(entry)]
        # FIXME plugin stuff
        # FIXME sorting
        return test_names


class MethodTestCase(ut2.TestCase):
    def __init__(self, cls, method):
        self.cls = cls
        self.method = method
        #self._
        #self._testMethodDoc = getattr(getattr(cls, method), '__doc__', None)
        self._name = "%s.%s.%s" % (cls.__module__, cls.__name__, method)
        ut2.TestCase.__init__(self, 'runTest')

    def __repr__(self):
        return self._name
    id = __str__ = __repr__

    def runTest(self):
        getattr(self.cls(), self.method)()

    # FIXME setup, teardown, class setup, class teardown
