import pathlib
import sys
import tempfile
import unittest

from nose2 import session
from nose2._toml import TOML_ENABLED
from nose2.tests._common import FunctionalTestCase, support_file


def test_loading_config_from_ini_file_without_cfg_suffix():
    """
    Regression test for https://github.com/nose-devs/nose2/issues/614

    It is possible to have nose2 config embedded in any ini config file, and it might
    not have a recognizable name.
    It is not guaranteed that filenames used for config will end in `.cfg`.
    """
    sess = session.Session()
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpdir = pathlib.Path(tmpdirname)

        foo_ini = tmpdir / "foo.ini"
        foo_ini.write_text("""[alpha]\na = 1""")

        sess.loadConfigFiles(str(foo_ini))
        assert sess.config.has_section("alpha")


class SessionFunctionalTests(FunctionalTestCase):
    def setUp(self):
        self.s = session.Session()
        self.s.loadConfigFiles(
            support_file("cfg", "a.cfg"), support_file("cfg", "b.cfg")
        )
        sys.path.insert(0, support_file("lib"))

    def test_session_can_load_config_files(self):
        assert self.s.config.has_section("a")
        assert self.s.config.has_section("b")

    def test_session_holds_plugin_config(self):
        plug_config = self.s.get("a")
        assert plug_config

    def test_session_can_load_plugins_from_modules(self):
        self.s.loadPlugins()
        assert self.s.plugins
        plug = self.s.plugins[0]
        self.assertEqual(plug.a, 1)

    def test_session_config_cacheing(self):
        """Test caching of config sections works"""

        # Create new session (generic one likely already cached
        # depending on test order)
        cache_sess = session.Session()
        cache_sess.loadConfigFiles(support_file("cfg", "a.cfg"))

        # First access to given section, should read from config file
        firstaccess = cache_sess.get("a")
        assert firstaccess.as_int("a") == 1

        # Hack cached Config object internals to make the stored value
        # something different
        cache_sess.configCache["a"]._mvd["a"] = "0"
        newitems = []
        for item in cache_sess.configCache["a"]._items:
            if item != ("a", "1"):
                newitems.append(item)
            else:
                newitems.append(("a", "0"))
        cache_sess.configCache["a"]._items = newitems

        # Second access to given section, confirm returns cached value
        # rather than parsing config file again
        secondaccess = cache_sess.get("a")
        assert secondaccess.as_int("a") == 0


class SessionTomlFunctionalTests(FunctionalTestCase):
    def setUp(self):
        if not TOML_ENABLED:
            raise unittest.SkipTest("toml module not available")
        self.s = session.Session()
        self.s.loadConfigFiles(
            support_file("toml", "a", "pyproject.toml"),
            support_file("toml", "b", "pyproject.toml"),
        )

    def test_session_can_load_config_files(self):
        assert self.s.config.has_section("a")
        assert self.s.config.has_section("b")

    def test_session_holds_plugin_config(self):
        plug_config = self.s.get("a")
        assert plug_config

    def test_session_can_load_toml_plugins_from_modules(self):
        self.s.loadPlugins()
        assert self.s.plugins
        plug = self.s.plugins[0]
        self.assertEqual(plug.a, 1)

    def test_session_config_cacheing(self):
        """Test caching of config sections works"""

        # Create new session (generic one likely already cached
        # depending on test order)
        cache_sess = session.Session()
        cache_sess.loadConfigFiles(support_file("toml", "a", "pyproject.toml"))

        # First access to given section, should read from config file
        firstaccess = cache_sess.get("a")
        assert firstaccess.as_int("a") == 1
        # Hack cached Config object internals to make the stored value
        # something different
        cache_sess.configCache["a"]._mvd["a"] = "0"
        newitems = []
        for item in cache_sess.configCache["a"]._items:
            if item != ("a", "1"):
                newitems.append(item)
            else:
                newitems.append(("a", "0"))
        cache_sess.configCache["a"]._items = newitems

        # Second access to given section, confirm returns cached value
        # rather than parsing config file again
        secondaccess = cache_sess.get("a")
        assert secondaccess.as_int("a") == 0
