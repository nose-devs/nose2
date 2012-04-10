from nose2 import events
from nose2.compat import unittest
from nose2.tools import such


REQUIRE = ['nose2.plugins.layers']


class SuchLoader(events.Plugin):
    alwaysOn = False
    configSection = 'such'
    commandLineSwitch = (None, 'such', 'Load tests written using "such" DSL')

    def generateModuleTests(self, event):
        module = event.module
        for entry in dir(module):
            item = getattr(module, entry)
            if isinstance(item, such.Scenario):
                self._generateScenarioTests(event.module, item)

    def _generateScenarioTests(self, module, scenario):
        # walk the group list
        # for each group, make a layer, layer suite, and test case class
        # attach a test method for each test
        # add test case instance bound to each method to layer suite
        # put child layer suite under parent
        # return top-level layer suite
        return self._makeGroupTest(module, scenario._group)

    def _makeGroupTest(self, module, group, parent_layer=None):
        layer = self._makeLayer(group, parent_layer)
        case = self._makeTestCase(group, layer)
        setattr(module, layer.__name__, layer)
        layer.__module__ = module.__name__
        setattr(module, case.__name__, case)
        case.__module__ = module.__name__

        for child in group._children:
            self._makeGroupTest(module, child, layer)

    def _makeTestCase(self, group, layer):
        attr = {
            'layer': layer,
            'group': group,
            'description': group.description,
            }

        for case in group._cases:
            def _test(s, case=case):
                case()
            name = 'test: %s' % case.description
            _test.__name__ = name
            _test.description = case.description
            _test.case = case
            attr[name] = _test
        return type(group.description, (unittest.TestCase,), attr)

    def _makeLayer(self, group, parent_layer=None):
        if parent_layer is None:
            parent_layer = object

        # FIXME test setups
        #test_setups = group._test_setups[:]
        #test_teardowns = group._testeardowns[:]

        def setUp(cls):
            for setup in cls.setups:
                setup()

        def tearDown(cls):
            for teardown in cls.teardowns:
                teardown()

        attr = {
            'setUp': classmethod(setUp),
            'tearDown': classmethod(tearDown),
            'setups': group._setups[:],
            'teardowns': group._teardowns[:],
            }

        return type("%s:layer" % group.description, (parent_layer, ), attr)
