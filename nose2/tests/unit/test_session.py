import unittest

from nose2 import events, session


class SessionUnitTests(unittest.TestCase):
    def test_can_create_session(self):
        session.Session()

    def test_load_plugins_from_module_can_load_plugins(self):
        class fakemod:
            pass

        f = fakemod()

        class A(events.Plugin):
            pass

        f.A = A
        s = session.Session()
        s.loadPluginsFromModule(f)
        assert s.plugins
        a = s.plugins[0]
        self.assertEqual(a.session, s)

    def test_load_plugins_from_module_does_not_load_plain_Plugins(self):
        class fakemod:
            pass

        f = fakemod()

        f.A = events.Plugin
        s = session.Session()
        s.loadPluginsFromModule(f)
        self.assertEqual(len(s.plugins), 0)

    def test_load_plugins_from_module_does_not_duplicate_always_on_plugins(self):
        class fakemod:
            pass

        f = fakemod()

        class A(events.Plugin):
            alwaysOn = True

        f.A = A
        s = session.Session()
        s.loadPluginsFromModule(f)
        self.assertEqual(len(s.plugins), 1)
