import sys

from nose2 import session
from nose2.tests._common import support_file, FunctionalTestCase


class SessionFunctionalTests(FunctionalTestCase):

    def setUp(self):
        self.s = session.Session()
        self.s.loadConfigFiles(support_file('cfg', 'a.cfg'),
                               support_file('cfg', 'b.cfg'))
        sys.path.insert(0, support_file('lib'))

    def test_session_can_load_config_files(self):
        assert self.s.config.has_section('a')
        assert self.s.config.has_section('b')

    def test_session_holds_plugin_config(self):
        plug_config = self.s.get('a')
        assert plug_config

    def test_session_can_load_plugins_from_modules(self):
        self.s.loadPlugins()
        assert self.s.plugins
        plug = self.s.plugins[0]
        self.assertEqual(plug.a, 1)

    def test_session_config_cacheing(self):
        """Test cacheing of config sections works"""

        # Create new session (generic one likely already cached
        # depending on test order)
        cachesess = session.Session()
        cachesess.loadConfigFiles(support_file('cfg', 'a.cfg'))

        # First access to given section, should read from config file
        firstaccess = cachesess.get('a')
        assert firstaccess.as_int("a") == 1

        # Hack cached Config object internals to make the stored value
        # something different
        cachesess.configCache["a"]._mvd["a"] = "0"
        newitems = []
        for item in cachesess.configCache["a"]._items:
            if item != ("a", "1"):
                newitems.append(item)
            else:
                newitems.append(("a", "0"))
        cachesess.configCache["a"]._items = newitems

        # Second access to given section, confirm returns cached value
        # rather than parsing config file again
        secondaccess = cachesess.get("a")
        assert secondaccess.as_int("a") == 0


