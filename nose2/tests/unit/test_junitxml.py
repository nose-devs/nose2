import datetime
import logging
import os
import sys
import time
import unittest
from xml.etree import ElementTree as ET

from nose2 import events, loader, result, session, tools
from nose2.plugins import junitxml, logcapture
from nose2.plugins.loader import functions, generators, parameters, testcases
from nose2.tests._common import TestCase


def _fromisoformat(date_str):
    # use fromisoformat when it is available, but failover to strptime for python2 and
    # older python3 versions
    if hasattr(datetime.datetime, "fromisoformat"):
        return datetime.datetime.fromisoformat(date_str)
    return datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")


class TestJunitXmlPlugin(TestCase):
    _RUN_IN_TEMP = True

    BAD_FOR_XML_U = "A\x07 B\x0b C\x10 D\ud900 E\ufffe F\x80 G\x90 H\ufddd"
    # UTF-8 string with double null (invalid)
    BAD_FOR_XML_B = (
        b"A\x07 B\x0b C\x10 D\xed\xa4\x80 "
        b"E\xef\xbf\xbe F\xc2\x80 G\xc2\x90 H\xef\xb7\x9d "
        b"\x00\x00"
    )

    # "byte" strings in PY2 and unicode in py3 works as expected will
    # will translate surrogates into UTF-16 characters  so BAD_FOR_XML_U
    # should have 8 letters follows by 0xFFFD, but only 4 when keeping
    # the discouraged/restricted ranges. Respectively:
    # "A\uFFFD B\uFFFD C\uFFFD D\uFFFD E\uFFFD F\uFFFD G\uFFFD H\uFFFD"
    # "A\uFFFD B\uFFFD C\uFFFD D\uFFFD E\uFFFD F\x80 G\x90 H\uFDDD"
    #
    # In Python 2 Invalid ascii characters seem to get escaped out as part
    # of tracebace.format_traceback so full and partial replacements are:
    # "A\uFFFD B\uFFFD C\uFFFD D\\\\ud900 E\\\\ufffe F\\\\x80 G\\\\x90 H\\\\ufddd"
    # "A\uFFFD B\uFFFD C\uFFFD D\\\\ud900 E\\\\ufffe F\\\\x80 G\\\\x90 H\\\\ufddd"
    #
    # Byte strings in py3 as errors are replaced by their representation string
    # So these will be safe and not have any replacements
    # "b'A\\x07 B\\x0b C\\x10 D\\xed\\xa4\\x80 E\\xef\\xbf\\xbe F\\xc2\\x80
    # G\\xc2\\x90 H\\xef\\xb7\\x9d \\x00\\x00"

    if sys.maxunicode <= 0xFFFF:
        EXPECTED_RE = "^[\x09\x0a\x0d\x20\x21-\ud7ff\ue000-\ufffd]*$"
        EXPECTED_RE_SAFE = (
            "^[\x09\x0a\x0d\x20\x21-\x7e\x85\xa0-\ud7ff\ue000-\ufdcf\ufdf0-\ufffd]*$"
        )
    else:
        EXPECTED_RE = "^[\x09\x0a\x0d\x20\x21-\ud7ff\ue000-\ufffd\u10000-\u10ffFF]*$"
        EXPECTED_RE_SAFE = (
            "^[\x09\x0a\x0d\x20\x21-\x7e\x85"
            "\xa0-\ud7ff\ue000-\ufdcf\ufdf0-\ufffd"
            "\u10000-\u1fffD\u20000-\u2fffD"
            "\u30000-\u3fffD\u40000-\u4fffD"
            "\u50000-\u5fffD\u60000-\u6fffD"
            "\u70000-\u7fffD\u80000-\u8fffD"
            "\u90000-\u8fffD\ua0000-\uafffD"
            "\ub0000-\ubfffD\uc0000-\ucfffD"
            "\ud0000-\udfffD\ue0000-\uefffD"
            "\uf0000-\uffffD\u100000-\u10ffFD]*$"
        )

    def setUp(self):
        super().setUp()
        self.session = session.Session()
        self.loader = loader.PluggableTestLoader(self.session)
        self.result = result.PluggableTestResult(self.session)
        self.plugin = junitxml.JUnitXmlReporter(session=self.session)
        self.plugin.register()

        class Test(unittest.TestCase):
            def test(self):
                pass

            def test_chdir(self):
                TEMP_SUBFOLDER = "test_chdir"

                os.mkdir(TEMP_SUBFOLDER)
                os.chdir(TEMP_SUBFOLDER)

            def test_fail(self):
                assert False

            def test_err(self):
                1 / 0  # noqa: B018 useless expression

            def test_skip(self):
                self.skipTest("skip")

            def test_skip_no_reason(self):
                self.skipTest("")

            def test_bad_xml(self):
                raise RuntimeError(TestJunitXmlPlugin.BAD_FOR_XML_U)

            def test_bad_xml_b(self):
                raise RuntimeError(TestJunitXmlPlugin.BAD_FOR_XML_B)

            def test_gen(self):
                def check(a, b):
                    # workaround:
                    # for the test which ensures that the timestamp increases between
                    # generator test runs, insert a very small sleep
                    #
                    # on py3.10 on Windows, we have observed both of these tests getting
                    # the same timestamp
                    time.sleep(0.001)
                    self.assertEqual(a, b)

                yield check, 1, 1
                yield check, 1, 2

            @tools.params(1, 2, 3)
            def test_params(self, p):
                self.assertEqual(p, 2)

            def test_with_log(self):
                logging.info("log message")

        self.case = Test

    def test_success_added_to_xml(self):
        test = self.case("test")
        test(self.result)
        self.assertEqual(self.plugin.numtests, 1)
        self.assertEqual(len(self.plugin.tree.findall("testcase")), 1)

    def test_failure_includes_traceback(self):
        test = self.case("test_fail")
        test(self.result)
        case = self.plugin.tree.find("testcase")
        failure = case.find("failure")
        assert failure is not None
        assert "Traceback" in failure.text

    def test_error_bad_xml(self):
        self.plugin.keep_restricted = False
        test = self.case("test_bad_xml")
        test(self.result)
        case = self.plugin.tree.find("testcase")
        error = case.find("error")
        self.assertRegex(error.text, self.EXPECTED_RE_SAFE)

    def test_error_bad_xml_keep(self):
        self.plugin.keep_restricted = True
        test = self.case("test_bad_xml")
        test(self.result)
        case = self.plugin.tree.find("testcase")
        error = case.find("error")
        self.assertRegex(error.text, self.EXPECTED_RE)

    def test_error_bad_xml_b(self):
        self.plugin.keep_restricted = False
        test = self.case("test_bad_xml_b")
        test(self.result)
        case = self.plugin.tree.find("testcase")
        error = case.find("error")
        assert error is not None
        self.assertRegex(error.text, self.EXPECTED_RE_SAFE)

    def test_error_bad_xml_b_keep(self):
        self.plugin.keep_restricted = True
        test = self.case("test_bad_xml_b")
        test(self.result)
        case = self.plugin.tree.find("testcase")
        error = case.find("error")
        assert error is not None
        self.assertRegex(error.text, self.EXPECTED_RE)

    def test_error_includes_traceback(self):
        test = self.case("test_err")
        test(self.result)
        case = self.plugin.tree.find("testcase")
        error = case.find("error")
        assert error is not None
        assert "Traceback" in error.text

    def test_skip_includes_skipped(self):
        test = self.case("test_skip")
        test(self.result)
        case = self.plugin.tree.find("testcase")
        skip = case.find("skipped")
        assert skip is not None
        self.assertEqual(skip.get("message"), "test skipped: skip")
        self.assertEqual(skip.text, "skip")

    def test_skip_includes_skipped_no_reason(self):
        test = self.case("test_skip_no_reason")
        test(self.result)
        case = self.plugin.tree.find("testcase")
        skip = case.find("skipped")
        assert skip is not None
        self.assertIsNone(skip.get("message"))
        self.assertIsNone(skip.text)

    def test_generator_timestamp_increases(self):
        gen = generators.Generators(session=self.session)
        gen.register()
        event = events.LoadFromTestCaseEvent(self.loader, self.case)
        self.session.hooks.loadTestsFromTestCase(event)
        cases = event.extraTests
        for case in cases:
            case(self.result)
        xml = self.plugin.tree.findall("testcase")
        self.assertEqual(len(xml), 2)
        test1_timestamp_str = xml[0].get("timestamp")
        test1_timestamp = _fromisoformat(test1_timestamp_str)
        test2_timestamp_str = xml[1].get("timestamp")
        test2_timestamp = _fromisoformat(test2_timestamp_str)
        self.assertGreater(test2_timestamp, test1_timestamp)

    def test_generator_test_name_correct(self):
        gen = generators.Generators(session=self.session)
        gen.register()
        event = events.LoadFromTestCaseEvent(self.loader, self.case)
        self.session.hooks.loadTestsFromTestCase(event)
        cases = event.extraTests
        for case in cases:
            case(self.result)
        xml = self.plugin.tree.findall("testcase")
        self.assertEqual(len(xml), 2)
        self.assertEqual(xml[0].get("name"), "test_gen:1")
        self.assertEqual(xml[1].get("name"), "test_gen:2")

    def test_generator_test_full_name_correct(self):
        gen = generators.Generators(session=self.session)
        gen.register()
        self.plugin.test_fullname = True
        event = events.LoadFromTestCaseEvent(self.loader, self.case)
        self.session.hooks.loadTestsFromTestCase(event)
        cases = event.extraTests
        for case in cases:
            case(self.result)
        xml = self.plugin.tree.findall("testcase")
        self.assertEqual(len(xml), 2)
        self.assertEqual(xml[0].get("name"), "test_gen:1 (1, 1)")
        self.assertEqual(xml[1].get("name"), "test_gen:2 (1, 2)")

    def test_function_classname_is_module(self):
        fun = functions.Functions(session=self.session)
        fun.register()

        def test_func():
            pass

        cases = fun._createTests(test_func)
        self.assertEqual(len(cases), 1)
        cases[0](self.result)
        xml = self.plugin.tree.findall("testcase")
        self.assertEqual(len(xml), 1)
        self.assertTrue(xml[0].get("classname").endswith("test_junitxml"))

    def test_params_test_name_correct(self):
        # param test loading is a bit more complex than generator
        # loading. XXX -- can these be reconciled so they both
        # support exclude and also both support loadTestsFromTestCase?
        plug1 = parameters.Parameters(session=self.session)
        plug1.register()
        plug2 = testcases.TestCaseLoader(session=self.session)
        plug2.register()
        # need module to fire top-level event

        class Mod:
            pass

        m = Mod()
        m.Test = self.case
        event = events.LoadFromModuleEvent(self.loader, m)
        self.session.hooks.loadTestsFromModule(event)
        for case in event.extraTests:
            case(self.result)
        xml = self.plugin.tree.findall("testcase")
        self.assertEqual(len(xml), 13)
        params = [x for x in xml if x.get("name").startswith("test_params")]
        self.assertEqual(len(params), 3)
        self.assertEqual(params[0].get("name"), "test_params:1")
        self.assertEqual(params[1].get("name"), "test_params:2")
        self.assertEqual(params[2].get("name"), "test_params:3")

    def test_params_test_full_name_correct(self):
        plug1 = parameters.Parameters(session=self.session)
        plug1.register()
        plug2 = testcases.TestCaseLoader(session=self.session)
        plug2.register()
        # need module to fire top-level event

        class Mod:
            pass

        m = Mod()
        m.Test = self.case
        event = events.LoadFromModuleEvent(self.loader, m)
        self.plugin.test_fullname = True
        self.session.hooks.loadTestsFromModule(event)
        for case in event.extraTests:
            case(self.result)
        xml = self.plugin.tree.findall("testcase")
        self.assertEqual(len(xml), 13)
        params = [x for x in xml if x.get("name").startswith("test_params")]
        self.assertEqual(len(params), 3)
        self.assertEqual(params[0].get("name"), "test_params:1 (1)")
        self.assertEqual(params[1].get("name"), "test_params:2 (2)")
        self.assertEqual(params[2].get("name"), "test_params:3 (3)")

    def test_writes_xml_file_at_end(self):
        test = self.case("test")
        test(self.result)
        event = events.StopTestRunEvent(None, self.result, 1, 1)
        self.plugin.stopTestRun(event)
        with open(self.plugin.path) as fh:
            tree = ET.parse(fh).getroot()
        self.assertEqual(len(tree.findall("testcase")), 1)
        case = tree.find("testcase")
        assert "time" in case.attrib
        assert "timestamp" in case.attrib
        assert "classname" in case.attrib
        self.assertEqual(case.get("name"), "test")
        self.assertEqual(tree.get("errors"), "0")
        self.assertEqual(tree.get("failures"), "0")
        self.assertEqual(tree.get("skipped"), "0")
        self.assertEqual(tree.get("tests"), "1")
        assert "time" in tree.attrib

    def test_xml_file_path_is_not_affected_by_chdir_in_test(self):
        initial_dir = os.path.realpath(os.getcwd())
        test = self.case("test_chdir")
        test(self.result)
        plugin_dir = os.path.realpath(os.path.dirname(self.plugin.path))
        assert initial_dir == plugin_dir, self.plugin.path

    def test_xml_contains_empty_system_out_without_logcapture(self):
        test = self.case("test_with_log")
        test(self.result)
        case = self.plugin.tree.find("testcase")
        system_out = case.find("system-out")
        assert system_out is not None
        assert not system_out.text

    def test_xml_contains_log_message_in_system_out_with_logcapture(self):
        self.logcapture_plugin = logcapture.LogCapture(session=self.session)
        self.logcapture_plugin.register()

        test = self.case("test_with_log")
        test(self.result)
        case = self.plugin.tree.find("testcase")
        system_out = case.find("system-out")
        assert system_out is not None
        assert "log message" in system_out.text
        assert "INFO" in system_out.text
