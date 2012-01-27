from xml.etree import ElementTree as ET
from nose2.tests._common import TestCase
from nose2.compat import unittest
from nose2 import events, loader, result, session, tools
from nose2.plugins import junitxml
from nose2.plugins.loader import generators, parameters, testcases


class TestJunitXmlPlugin(TestCase):
    _RUN_IN_TEMP = True

    def setUp(self):
        super(TestJunitXmlPlugin, self).setUp()
        self.session = session.Session()
        self.loader = loader.PluggableTestLoader(self.session)
        self.result = result.PluggableTestResult(self.session)
        self.plugin = junitxml.JUnitXmlReporter(session=self.session)
        self.plugin.register()

        class Test(unittest.TestCase):
            def test(self):
                pass
            def test_fail(self):
                assert False
            def test_err(self):
                1/0
            def test_skip(self):
                raise unittest.SkipTest('skip')
            def test_gen(self):
                def check(a, b):
                    self.assertEqual(a, b)
                yield check, 1, 1
                yield check, 1, 2
            @tools.params(1, 2, 3)
            def test_params(self, p):
                self.assertEqual(p, 2)
        self.case = Test

    def test_success_added_to_xml(self):
        test = self.case('test')
        test(self.result)
        self.assertEqual(self.plugin.numtests, 1)
        self.assertEqual(len(self.plugin.tree.findall('testcase')), 1)

    def test_failure_includes_traceback(self):
        test = self.case('test_fail')
        test(self.result)
        case = self.plugin.tree.find('testcase')
        failure = case.find('failure')
        assert failure is not None
        assert 'Traceback' in failure.text

    def test_error_includes_traceback(self):
        test = self.case('test_err')
        test(self.result)
        case = self.plugin.tree.find('testcase')
        error = case.find('error')
        assert error is not None
        assert 'Traceback' in error.text

    def test_skip_includes_skipped(self):
        test = self.case('test_skip')
        test(self.result)
        case = self.plugin.tree.find('testcase')
        skip = case.find('skipped')
        assert skip is not None

    def test_generator_test_name_correct(self):
        gen = generators.Generators(session=self.session)
        gen.register()
        event = events.LoadFromTestCaseEvent(self.loader, self.case)
        self.session.hooks.loadTestsFromTestCase(event)
        cases = event.extraTests
        for case in cases:
            case(self.result)
        xml = self.plugin.tree.findall('testcase')
        self.assertEqual(len(xml), 2)
        self.assertEqual(xml[0].get('name'), 'test_gen:1')
        self.assertEqual(xml[1].get('name'), 'test_gen:2')

    def test_params_test_name_correct(self):
        # param test loading is a bit more complex than generator
        # loading. XXX -- can these be reconciled so they both
        # support exclude and also both support loadTestsFromTestCase?
        plug1 = parameters.Parameters(session=self.session)
        plug1.register()
        plug2 = testcases.TestCaseLoader(session=self.session)
        plug2.register()
        # need module to fire top-level event
        class Mod(object):
            pass
        m = Mod()
        m.Test = self.case
        event = events.LoadFromModuleEvent(self.loader, m)
        self.session.hooks.loadTestsFromModule(event)
        for case in event.extraTests:
            case(self.result)
        xml = self.plugin.tree.findall('testcase')
        self.assertEqual(len(xml), 8)
        params = [x for x in xml if x.get('name').startswith('test_params')]
        self.assertEqual(len(params), 3)
        self.assertEqual(params[0].get('name'), 'test_params:1')
        self.assertEqual(params[1].get('name'), 'test_params:2')
        self.assertEqual(params[2].get('name'), 'test_params:3')

    def test_writes_xml_file_at_end(self):
        test = self.case('test')
        test(self.result)
        event = events.StopTestRunEvent(None, self.result, 1, 1)
        self.plugin.stopTestRun(event)
        with open(self.plugin.path, 'r') as fh:
            tree = ET.parse(fh).getroot()
        self.assertEqual(len(tree.findall('testcase')), 1)
        case = tree.find('testcase')
        assert 'time' in case.attrib
        assert 'classname' in case.attrib
        self.assertEqual(case.get('name'), 'test')
        self.assertEqual(tree.get('errors'), '0')
        self.assertEqual(tree.get('failures'), '0')
        self.assertEqual(tree.get('skips'), '0')
        self.assertEqual(tree.get('tests'), '1')
        assert 'time' in tree.attrib

