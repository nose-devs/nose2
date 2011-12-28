import sys

from nose2.compat import unittest
from nose2 import config
from nose2.tests.functional import support_file


class TestConfigLoading(unittest.TestCase):

    def setUp(self):
        self.s = config.Session()
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
