import unittest

from nose2 import events, util
from nose2.compat import unittest as ut2

__unittest = True


class TestClasses(events.Plugin):
    alwaysOn = True
    configSection = 'test-classes'

    def pluginsLoaded(self, event):
        self.addMethods('loadTestsFromTestClass', 'getTestMethodNames')

    def loadTestsFromModule(self, event):
        module = event.module
        for name in dir(module):
            obj = getattr(module, name)
            if (isinstance(obj, type) and not
                issubclass(obj, unittest.TestCase) and not
                issubclass(obj, unittest.TestSuite) and
                name.lower().startswith(self.session.testMethodPrefix)):
                event.extraTests.append(
                    self._loadTestsFromTestClass(event, obj))

    def loadTestsFromName(self, event):
        """Load tests from event.name if it names a test case/method"""
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
        if isinstance(obj, type) and not issubclass(obj, unittest.TestCase):
            # name is a test case class
            event.extraTests.append(self._loadTestsFromTestClass(event, obj))
        elif (isinstance(parent, type) and
              not issubclass(parent, unittest.TestCase) and not
              util.isgenerator(obj) and not
              hasattr(obj, 'paramList')):
            # name is a single test method
            event.extraTests.append(
                util.transplant_class(
                    MethodTestCase(parent), parent.__module__)(obj.__name__))

    def _loadTestsFromTestClass(self, event, cls):
        # ... fire event for others to load from
        evt = LoadFromTestClassEvent(event.loader, cls)
        result = self.session.hooks.loadTestsFromTestClass(evt)
        if evt.handled:
            loaded_suite = result or event.loader.suiteClass()
        else:
            names = self._getTestMethodNames(event, cls)
            loaded_suite = event.loader.suiteClass(
                [util.transplant_class(
                        MethodTestCase(cls), cls.__module__)(name)
                 for name in names])
        if evt.extraTests:
            loaded_suite.addTests(evt.extraTests)
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
        evt = GetTestMethodNamesEvent(event.loader, cls, isTestMethod)
        result = self.session.hooks.getTestMethodNames(evt)
        if evt.handled:
            test_names = result or []
        else:
            excluded.update(evt.excludedNames)

            test_names = [entry for entry in dir(cls)
                          if isTestMethod(entry)]

        if event.loader.sortTestMethodsUsing:
            test_names.sort(key=event.loader.sortTestMethodsUsing)
        return test_names


# to prevent unit2 discover from running this as a test, need to
# hide it inside of a factory func. ugly!
def MethodTestCase(cls):
    class _MethodTestCase(ut2.TestCase):
        def __init__(self, method):
            self.method = method
            self._name = "%s.%s.%s" % (cls.__module__, cls.__name__, method)
            self.obj = cls()
            ut2.TestCase.__init__(self, 'runTest')

        @classmethod
        def setUpClass(klass):
            if hasattr(cls, 'setUpClass'):
                cls.setUpClass()

        @classmethod
        def tearDownClass(klass):
            if hasattr(cls, 'tearDownClass'):
                cls.tearDownClass()

        def setUp(self):
            if hasattr(self.obj, 'setUp'):
                self.obj.setUp()

        def tearDown(self):
            if hasattr(self.obj, 'tearDown'):
                self.obj.tearDown()

        def __repr__(self):
            return self._name
        id = __str__ = __repr__

        def runTest(self):
            getattr(self.obj, self.method)()

    return _MethodTestCase

#
# Event classes
# FIXME docs
#
class LoadFromTestClassEvent(events.LoadFromTestCaseEvent):
    pass


class GetTestMethodNamesEvent(events.GetTestCaseNamesEvent):
    pass
