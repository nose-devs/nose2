import os
from xml.etree import ElementTree as ET

from nose2.tests._common import FunctionalTestCase, TestCase, _method_name, support_file


class JunitXmlPluginFunctionalTest(FunctionalTestCase, TestCase):
    _RUN_IN_TEMP = True

    def run_with_junitxml_loaded(self, scenario, *args, **kwargs):
        work_dir = os.getcwd()
        test_dir = support_file(*scenario)
        junit_report = os.path.join(
            work_dir, kwargs.get("junit_report", "nose2-junit.xml")
        )
        config = os.path.join(test_dir, "unittest.cfg")
        config_args = ()
        if os.path.exists(junit_report):
            os.remove(junit_report)
        if os.path.exists(config):
            config_args = ("-c", config)
        proc = self.runIn(
            work_dir,
            "-s%s" % test_dir,
            "--plugin=nose2.plugins.junitxml",
            "-v",
            *(config_args + args),
        )
        return junit_report, proc

    def test_invocation_by_double_dash_option(self):
        junit_report, proc = self.run_with_junitxml_loaded(
            ("scenario", "junitxml", "happyday"), "--junit-xml"
        )

        self.assertTestRunOutputMatches(
            proc,
            stderr=r"test \(test_junitxml_happyday.Test"
            + _method_name()
            + r"\) ... ok",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertEqual(proc.poll(), 0)

        self.assertTrue(
            os.path.isfile(junit_report),
            "junitxml report wasn't found in working directory. "
            "Searched for " + junit_report,
        )

    def test_invocation_by_single_dash_option(self):
        junit_report, proc = self.run_with_junitxml_loaded(
            ("scenario", "junitxml", "happyday"), "-X"
        )

        self.assertTestRunOutputMatches(
            proc,
            stderr=r"test \(test_junitxml_happyday.Test"
            + _method_name()
            + r"\) ... ok",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertEqual(proc.poll(), 0)

        self.assertTrue(
            os.path.isfile(junit_report),
            "junitxml report wasn't found in working directory. "
            "Searched for " + junit_report,
        )

    def test_implicit_registration_by_path_option(self):
        junit_report, proc = self.run_with_junitxml_loaded(
            ("scenario", "junitxml", "happyday"),
            "--junit-xml-path=b.xml",
            junit_report="b.xml",
        )

        self.assertTestRunOutputMatches(
            proc,
            stderr=r"test \(test_junitxml_happyday.Test"
            + _method_name()
            + r"\) ... ok",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertEqual(proc.poll(), 0)

        self.assertTrue(
            os.path.isfile(junit_report),
            "junitxml report wasn't found in working directory. "
            "Searched for " + junit_report,
        )

    def test_no_report_written_if_loaded_but_not_invoked(self):
        junit_report, proc = self.run_with_junitxml_loaded(
            ("scenario", "junitxml", "happyday")
        )

        self.assertTestRunOutputMatches(
            proc,
            stderr=r"test \(test_junitxml_happyday.Test"
            + _method_name()
            + r"\) ... ok",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertEqual(proc.poll(), 0)

        self.assertFalse(
            os.path.isfile(junit_report),
            "junitxml report was found in working directory. "
            "Report file: " + junit_report,
        )

    def test_report_location_should_be_resilent_to_chdir_in_tests(self):
        junit_report, proc = self.run_with_junitxml_loaded(
            ("scenario", "junitxml", "chdir"), "--junit-xml"
        )

        self.assertTestRunOutputMatches(
            proc,
            stderr=r"test_chdir \(test_junitxml_chdir.Test"
            + _method_name("test_chdir")
            + r"\) \.* ok",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertEqual(proc.poll(), 0)

        self.assertTrue(
            os.path.isfile(junit_report),
            "junitxml report wasn't found in working directory. "
            "Searched for " + junit_report,
        )

    def test_report_includes_properties(self):
        work_dir = os.getcwd()
        with open(os.path.join(work_dir, "properties.json"), "w") as fh:
            fh.write('{"PROPERTY_NAME":"PROPERTY_VALUE"}')
        junit_report, proc = self.run_with_junitxml_loaded(
            ("scenario", "junitxml", "with_properties"), "--junit-xml"
        )
        self.assertTestRunOutputMatches(
            proc,
            stderr=r"test \(test_junitxml_with_properties.Test"
            + _method_name()
            + r"\) \.* ok",
        )
        self.assertEqual(proc.poll(), 0)

        with open(junit_report) as fh:
            tree = ET.parse(fh).getroot()
        self.assertEqual(len(tree.findall("properties")), 1)
        prop = tree.find("properties").find("property")
        assert "name" in prop.attrib
        assert "value" in prop.attrib
        self.assertEqual(prop.get("name"), "PROPERTY_NAME")
        self.assertEqual(prop.get("value"), "PROPERTY_VALUE")

    def test_skip_reason_in_message(self):
        junit_report, proc = self.run_with_junitxml_loaded(
            ("scenario", "junitxml", "skip_reason"), "--junit-xml"
        )

        self.assertTestRunOutputMatches(
            proc,
            stderr=r"test \(test_junitxml_skip_reason.Test"
            + _method_name()
            + r"\) \.* skip",
        )

        exit_status = proc.poll()
        assert exit_status == 0

        with open(junit_report) as fh:
            tree = ET.parse(fh).getroot()

        num_test_cases = len(tree.findall("testcase"))
        assert num_test_cases == 1

        num_skipped = len(tree.find("testcase").findall("skipped"))
        assert num_skipped == 1
        skip_node = tree.find("testcase").find("skipped")
        assert "message" in skip_node.attrib
        skip_message = skip_node.get("message")
        assert skip_message == "test skipped: ohai"

    def test_xml_path_override_by_config(self):
        junit_report, proc = self.run_with_junitxml_loaded(
            ("scenario", "junitxml", "non_default_path"),
            "--junit-xml",
            junit_report="a.xml",
        )

        self.assertTestRunOutputMatches(
            proc,
            stderr=r"test \(test_junitxml_non_default_path.Test"
            + _method_name()
            + r"\) \.* ok",
        )

        exit_status = proc.poll()
        assert exit_status == 0

        self.assertTrue(os.path.isfile(junit_report))

    def test_xml_path_override_by_command(self):
        junit_report, proc = self.run_with_junitxml_loaded(
            ("scenario", "junitxml", "non_default_path"),
            "--junit-xml",
            "--junit-xml-path=b.xml",
            junit_report="b.xml",
        )

        self.assertTestRunOutputMatches(
            proc,
            stderr=r"test \(test_junitxml_non_default_path.Test"
            + _method_name()
            + r"\) \.* ok",
        )

        exit_status = proc.poll()
        assert exit_status == 0

        self.assertTrue(os.path.isfile(junit_report))


class JunitXmlPluginFunctionalFailureTest(FunctionalTestCase, TestCase):
    def test_failure_to_write_report(self):
        proc = self.runIn(
            "scenario/junitxml/fail_to_write",
            "--plugin=nose2.plugins.junitxml",
            "-v",
            "--junit-xml",
        )
        self.assertEqual(proc.poll(), 1)

        self.assertTestRunOutputMatches(
            proc,
            stderr=r"test \(test_junitxml_fail_to_write.Test"
            + _method_name()
            + r"\) \.* ok",
        )

        filename_for_regex = os.path.abspath("/does/not/exist.xml")
        filename_for_regex = filename_for_regex.replace("\\", r"\\\\")
        self.assertTestRunOutputMatches(
            proc,
            stderr=r"Internal Error: runTests aborted: \[Errno 2\] "
            "JUnitXML: Parent folder does not exist for file: "
            "'%s'" % filename_for_regex,
        )

    def test_failure_to_read_missing_properties(self):
        proc = self.runIn(
            "scenario/junitxml/missing_properties",
            "--plugin=nose2.plugins.junitxml",
            "-v",
            "--junit-xml",
        )
        self.assertEqual(proc.poll(), 1)

        self.assertTestRunOutputMatches(
            proc,
            stderr=r"test \(test_junitxml_missing_properties.Test"
            + _method_name()
            + r"\) \.* ok",
        )

        filename_for_regex = os.path.join("missing_properties", "properties.json")
        filename_for_regex = filename_for_regex.replace("\\", r"\\\\")
        self.assertTestRunOutputMatches(
            proc,
            stderr=r"Internal Error: runTests aborted: \[Errno 2\] "
            "JUnitXML: Properties file does not exist: "
            "'.*%s'" % filename_for_regex,
        )

    def test_failure_to_read_empty_properties(self):
        proc = self.runIn(
            "scenario/junitxml/empty_properties",
            "--plugin=nose2.plugins.junitxml",
            "-v",
            "--junit-xml",
        )
        self.assertEqual(proc.poll(), 1)

        self.assertTestRunOutputMatches(
            proc,
            stderr=r"test \(test_junitxml_empty_properties.Test"
            + _method_name()
            + r"\) \.* ok",
        )

        filename_for_regex = os.path.join("empty_properties", "properties.json")
        filename_for_regex = filename_for_regex.replace("\\", r"\\")
        self.assertTestRunOutputMatches(
            proc,
            stderr="Internal Error: runTests aborted: "
            "JUnitXML: could not decode file: "
            "'.*%s'" % filename_for_regex,
        )
