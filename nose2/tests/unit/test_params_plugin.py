from nose2 import events, loader, session, util
from nose2.plugins.loader import parameters, testcases
from nose2.tests._common import TestCase
from nose2.tools import cartesian_params, params


class TestParams(TestCase):
    tags = ['unit']

    def setUp(self):
        self.session = session.Session()
        self.loader = loader.PluggableTestLoader(self.session)
        self.plugin = parameters.Parameters(session=self.session)
        # need testcase loader to make the initial response to load from module
        self.tcl = testcases.TestCaseLoader(session=self.session)

    def test_ignores_ordinary_functions(self):
        class Mod(object):
            pass

        def test():
            pass
        m = Mod()
        m.test = test
        event = events.LoadFromModuleEvent(self.loader, m)
        self.session.hooks.loadTestsFromModule(event)
        self.assertEqual(len(event.extraTests), 0)

    def test_can_load_tests_from_parameterized_functions(self):
        class Mod(object):
            __name__ = 'themod'

        def check(x):
            assert x == 1

        @params(1, 2)
        def test(a):
            check(a)
        m = Mod()
        m.test = test
        test.__module__ = m.__name__
        event = events.LoadFromModuleEvent(self.loader, m)
        self.session.hooks.loadTestsFromModule(event)
        self.assertEqual(len(event.extraTests), 2)
        # check that test names are sensible
        self.assertEqual(util.test_name(event.extraTests[0]),
                         'themod.test:1')
        self.assertEqual(util.test_name(event.extraTests[1]),
                         'themod.test:2')

    def test_can_load_tests_from_parameterized_methods(self):
        class Mod(object):
            __name__ = 'themod'

        class Test(TestCase):

            @cartesian_params(
                (1, 2),
                (2, 3),
            )
            def test_cartesian_params(self, first, second):
                assert first == second

            @params(1, 2)
            def test_params(self, a):
                assert a == 1

        m = Mod()
        m.Test = Test
        Test.__module__ = m.__name__
        event = events.LoadFromModuleEvent(self.loader, m)
        self.session.hooks.loadTestsFromModule(event)
        self.assertEqual(len(event.extraTests), 1)
        self.assertEqual(len(event.extraTests[0]._tests), 2 + 4)
        # check @cartesian_params for that test names are sensible
        self.assertEqual(util.test_name(event.extraTests[0]._tests[0]),
                         'themod.Test.test_cartesian_params:1')
        self.assertEqual(util.test_name(event.extraTests[0]._tests[1]),
                         'themod.Test.test_cartesian_params:2')
        self.assertEqual(util.test_name(event.extraTests[0]._tests[2]),
                         'themod.Test.test_cartesian_params:3')
        self.assertEqual(util.test_name(event.extraTests[0]._tests[3]),
                         'themod.Test.test_cartesian_params:4')
        # check @params for that test names are sensible
        self.assertEqual(util.test_name(event.extraTests[0]._tests[4]),
                         'themod.Test.test_params:1')
        self.assertEqual(util.test_name(event.extraTests[0]._tests[5]),
                         'themod.Test.test_params:2')
