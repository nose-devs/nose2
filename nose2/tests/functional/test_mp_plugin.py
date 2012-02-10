import sys

from nose2 import session
from nose2.compat import unittest
from nose2.plugins.mp import MultiProcess
from nose2.tests._common import FunctionalTestCase, support_file



class TestMpPlugin(FunctionalTestCase):

    def setUp(self):
        super(TestMpPlugin, self).setUp()
        self.session = session.Session()
        self.plugin = MultiProcess(session=self.session)

    def test_flatten_without_fixtures(self):
        sys.path.append(support_file('scenario/slow'))
        import test_slow as mod

        suite = unittest.TestSuite()
        suite.addTest(mod.TestSlow('test_ok'))
        suite.addTest(mod.TestSlow('test_fail'))
        suite.addTest(mod.TestSlow('test_err'))

        flat = list(self.plugin._flatten(suite))
        self.assertEqual(len(flat), 3)

    def test_flatten_nested_suites(self):
        sys.path.append(support_file('scenario/slow'))
        import test_slow as mod

        suite = unittest.TestSuite()
        suite.addTest(mod.TestSlow('test_ok'))
        suite.addTest(mod.TestSlow('test_fail'))
        suite.addTest(mod.TestSlow('test_err'))

        suite2 = unittest.TestSuite()
        suite2.addTest(suite)

        flat = list(self.plugin._flatten(suite2))
        self.assertEqual(len(flat), 3)

    def test_flatten_respects_module_fixtures(self):
        sys.path.append(support_file('scenario/module_fixtures'))
        import test_mf_testcase as mod

        suite = unittest.TestSuite()
        suite.addTest(mod.Test('test_1'))
        suite.addTest(mod.Test('test_2'))

        flat = list(self.plugin._flatten(suite))
        self.assertEqual(flat, ['test_mf_testcase'])

    def test_flatten_respects_class_fixtures(self):
        sys.path.append(support_file('scenario/class_fixtures'))
        import test_cf_testcase as mod

        suite = unittest.TestSuite()
        suite.addTest(mod.Test('test_1'))
        suite.addTest(mod.Test('test_2'))
        suite.addTest(mod.Test2('test_1'))
        suite.addTest(mod.Test2('test_2'))

        flat = list(self.plugin._flatten(suite))
        self.assertEqual(flat, ['test_cf_testcase.Test2.test_1',
                                'test_cf_testcase.Test2.test_2',
                                'test_cf_testcase.Test',
                                ])
