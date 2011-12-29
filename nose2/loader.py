from nose2 import events
from nose2.compat import unittest


class PluggableTestLoader(object):
    """Test loader that defers all loading to plugins"""

    suiteClass = unittest.TestSuite

    def __init__(self, session):
        self.session = session

    def loadTestsFromModule(self, module):
        evt = events.LoadFromModuleEvent(self, module)
        self.session.hooks.loadTestsFromModule(evt)
        return self.suiteClass(evt.extraTests)

    def loadTestsFromNames(self, testNames, module=None):
        evt = events.LoadFromNamesEvent(
            self, testNames,module)
        self.session.hooks.loadTestsFromNames(evt)
        return self.suiteClass(evt.extraTests)
