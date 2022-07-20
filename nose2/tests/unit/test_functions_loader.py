import unittest
from unittest import mock

from nose2 import events, loader, session
from nose2.plugins.loader import functions
from nose2.tests._common import TestCase


class TestFunctionLoader(TestCase):
    def setUp(self):
        self.session = session.Session()
        self.loader = loader.PluggableTestLoader(self.session)
        self.plugin = functions.Functions(session=self.session)

    def test_can_load_test_functions_from_module(self):
        class Mod:
            pass

        def test():
            pass

        m = Mod()
        m.test = test
        event = events.LoadFromModuleEvent(self.loader, m)
        self.session.hooks.loadTestsFromModule(event)
        self.assertEqual(len(event.extraTests), 1)
        assert isinstance(event.extraTests[0], unittest.FunctionTestCase)

    def test_ignores_generator_functions(self):
        class Mod:
            pass

        def test():
            yield

        m = Mod()
        m.test = test
        event = events.LoadFromModuleEvent(self.loader, m)
        self.session.hooks.loadTestsFromModule(event)
        self.assertEqual(len(event.extraTests), 0)

    def test_ignores_functions_that_take_args(self):
        class Mod:
            pass

        def test(a):
            pass

        m = Mod()
        m.test = test
        event = events.LoadFromModuleEvent(self.loader, m)
        self.session.hooks.loadTestsFromModule(event)
        self.assertEqual(len(event.extraTests), 0)

    def test_can_load_test_functions_from_name(self):
        event = events.LoadFromNameEvent(self.loader, __name__ + ".func", None)
        suite = self.session.hooks.loadTestsFromName(event)
        self.assertNotEqual(suite, None)

    def test_ignores_test_methods_from_name(self):
        # Should ignore test methods even when specified directly
        event = events.LoadFromNameEvent(
            self.loader, __name__ + ".Case.test_method", None
        )
        suite = self.session.hooks.loadTestsFromName(event)
        self.assertEqual(suite, None)

    def test_ignores_decorated_test_methods_from_name(self):
        # Should ignore test methods even when they are of FunctionType
        event = events.LoadFromNameEvent(
            self.loader, __name__ + ".Case.test_patched", None
        )
        suite = self.session.hooks.loadTestsFromName(event)
        self.assertEqual(suite, None)


def func():
    pass


def dummy():
    pass


class Case(unittest.TestCase):
    __test__ = False  # do not run this

    def test_method(self):
        pass

    @mock.patch(__name__ + ".dummy")
    def test_patched(self, mock):
        pass
