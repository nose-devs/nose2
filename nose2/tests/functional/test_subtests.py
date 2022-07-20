import os
import tempfile
from xml.etree import ElementTree as ET

from nose2.tests._common import FunctionalTestCase


def read_report(path):
    with open(path, encoding="utf-8") as f:
        return ET.parse(f).getroot()


class TestSubtests(FunctionalTestCase):
    def test_success(self):
        proc = self.runIn(
            "scenario/subtests", "-v", "test_subtests.Case.test_subtest_success"
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertTestRunOutputMatches(proc, stderr="test_subtest_success")
        self.assertTestRunOutputMatches(proc, stderr="OK")
        self.assertEqual(proc.poll(), 0)

    def test_failure(self):
        proc = self.runIn(
            "scenario/subtests", "-v", "test_subtests.Case.test_subtest_failure"
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_failure.*\(i=1\)")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_failure.*\(i=3\)")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_failure.*\(i=5\)")
        self.assertTestRunOutputMatches(proc, stderr=r"FAILED \(failures=3\)")
        self.assertEqual(proc.poll(), 1)

    def test_error(self):
        proc = self.runIn(
            "scenario/subtests", "-v", "test_subtests.Case.test_subtest_error"
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_error.*\(i=0\)")
        self.assertTestRunOutputMatches(proc, stderr="RuntimeError: 0")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_error.*\(i=1\)")
        self.assertTestRunOutputMatches(proc, stderr="RuntimeError: 1")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_error.*\(i=2\)")
        self.assertTestRunOutputMatches(proc, stderr="RuntimeError: 2")
        self.assertTestRunOutputMatches(proc, stderr=r"FAILED \(errors=3\)")
        self.assertEqual(proc.poll(), 1)

    def test_expected_failure(self):
        proc = self.runIn(
            "scenario/subtests",
            "-v",
            "test_subtests.Case.test_subtest_expected_failure",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertTestRunOutputMatches(
            proc, stderr="test_subtest_expected_failure.*expected failure"
        )
        self.assertTestRunOutputMatches(proc, stderr=r"OK \(expected failures=1\)")
        self.assertEqual(proc.poll(), 0)

    def test_message(self):
        proc = self.runIn(
            "scenario/subtests", "-v", "test_subtests.Case.test_subtest_message"
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertTestRunOutputMatches(
            proc, stderr=r"test_subtest_message.*\[msg\] \(i=1\)"
        )
        self.assertTestRunOutputMatches(
            proc, stderr=r"test_subtest_message.*\[msg\] \(i=3\)"
        )
        self.assertTestRunOutputMatches(
            proc, stderr=r"test_subtest_message.*\[msg\] \(i=5\)"
        )
        self.assertTestRunOutputMatches(proc, stderr=r"FAILED \(failures=3\)")
        self.assertEqual(proc.poll(), 1)

    def test_all(self):
        proc = self.runIn("scenario/subtests", "-v", "test_subtests")
        self.assertTestRunOutputMatches(proc, stderr="Ran 5 tests")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_failure.*\(i=1\)")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_failure.*\(i=3\)")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_failure.*\(i=5\)")
        self.assertTestRunOutputMatches(
            proc, stderr=r"test_subtest_message.*\[msg\] \(i=1\)"
        )
        self.assertTestRunOutputMatches(
            proc, stderr=r"test_subtest_message.*\[msg\] \(i=3\)"
        )
        self.assertTestRunOutputMatches(
            proc, stderr=r"test_subtest_message.*\[msg\] \(i=5\)"
        )
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_error.*\(i=0\)")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_error.*\(i=1\)")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_error.*\(i=2\)")
        self.assertTestRunOutputMatches(
            proc, stderr=r"FAILED \(failures=6, errors=3, expected failures=1\)"
        )
        self.assertEqual(proc.poll(), 1)


class TestSubtestsMultiprocess(FunctionalTestCase):
    def test_success(self):
        proc = self.runIn(
            "scenario/subtests",
            "--plugin=nose2.plugins.mp",
            "--processes=2",
            "-v",
            "test_subtests.Case.test_subtest_success",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertTestRunOutputMatches(proc, stderr="test_subtest_success")
        self.assertTestRunOutputMatches(proc, stderr="OK")
        self.assertEqual(proc.poll(), 0)

    def test_failure(self):
        proc = self.runIn(
            "scenario/subtests",
            "--plugin=nose2.plugins.mp",
            "--processes=2",
            "-v",
            "test_subtests.Case.test_subtest_failure",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_failure.*\(i=1\)")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_failure.*\(i=3\)")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_failure.*\(i=5\)")
        self.assertTestRunOutputMatches(proc, stderr=r"FAILED \(failures=3\)")
        self.assertEqual(proc.poll(), 1)

    def test_error(self):
        proc = self.runIn(
            "scenario/subtests",
            "--plugin=nose2.plugins.mp",
            "--processes=2",
            "-v",
            "test_subtests.Case.test_subtest_error",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_error.*\(i=0\)")
        self.assertTestRunOutputMatches(proc, stderr="RuntimeError: 0")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_error.*\(i=1\)")
        self.assertTestRunOutputMatches(proc, stderr="RuntimeError: 1")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_error.*\(i=2\)")
        self.assertTestRunOutputMatches(proc, stderr="RuntimeError: 2")
        self.assertTestRunOutputMatches(proc, stderr=r"FAILED \(errors=3\)")
        self.assertEqual(proc.poll(), 1)

    def test_expected_failure(self):
        proc = self.runIn(
            "scenario/subtests",
            "--plugin=nose2.plugins.mp",
            "--processes=2",
            "-v",
            "test_subtests.Case.test_subtest_expected_failure",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertTestRunOutputMatches(
            proc, stderr="test_subtest_expected_failure.*expected failure"
        )
        self.assertTestRunOutputMatches(proc, stderr=r"OK \(expected failures=1\)")
        self.assertEqual(proc.poll(), 0)

    def test_message(self):
        proc = self.runIn(
            "scenario/subtests",
            "--plugin=nose2.plugins.mp",
            "--processes=2",
            "-v",
            "test_subtests.Case.test_subtest_message",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertTestRunOutputMatches(
            proc, stderr=r"test_subtest_message.*\[msg\] \(i=1\)"
        )
        self.assertTestRunOutputMatches(
            proc, stderr=r"test_subtest_message.*\[msg\] \(i=3\)"
        )
        self.assertTestRunOutputMatches(
            proc, stderr=r"test_subtest_message.*\[msg\] \(i=5\)"
        )
        self.assertTestRunOutputMatches(proc, stderr=r"FAILED \(failures=3\)")
        self.assertEqual(proc.poll(), 1)

    def test_all(self):
        proc = self.runIn(
            "scenario/subtests",
            "--plugin=nose2.plugins.mp",
            "--processes=2",
            "-v",
            "test_subtests",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 5 tests")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_failure.*\(i=1\)")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_failure.*\(i=3\)")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_failure.*\(i=5\)")
        self.assertTestRunOutputMatches(
            proc, stderr=r"test_subtest_message.*\[msg\] \(i=1\)"
        )
        self.assertTestRunOutputMatches(
            proc, stderr=r"test_subtest_message.*\[msg\] \(i=3\)"
        )
        self.assertTestRunOutputMatches(
            proc, stderr=r"test_subtest_message.*\[msg\] \(i=5\)"
        )
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_error.*\(i=0\)")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_error.*\(i=1\)")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_error.*\(i=2\)")
        self.assertTestRunOutputMatches(
            proc, stderr=r"FAILED \(failures=6, errors=3, expected failures=1\)"
        )
        self.assertEqual(proc.poll(), 1)


class TestSubtestsJunitXml(FunctionalTestCase):
    def setUp(self):
        super().setUp()
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.close()
        self.junit_report = tmp.name

    def tearDown(self):
        os.remove(self.junit_report)

    def test_success(self):
        proc = self.runIn(
            "scenario/subtests",
            "--plugin=nose2.plugins.junitxml",
            "--junit-xml",
            f"--junit-xml-path={self.junit_report}",
            "-v",
            "test_subtests.Case.test_subtest_success",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertTestRunOutputMatches(proc, stderr="OK")
        self.assertEqual(proc.poll(), 0)

        tree = read_report(self.junit_report)
        self.assertEqual(tree.get("tests"), "1")
        self.assertEqual(tree.get("failures"), "0")
        self.assertEqual(tree.get("errors"), "0")
        self.assertEqual(tree.get("skipped"), "0")
        self.assertEqual(len(tree.findall("testcase")), 1)

        for test_case in tree.findall("testcase"):
            self.assertEqual(test_case.get("name"), "test_subtest_success")

    def test_failure(self):
        proc = self.runIn(
            "scenario/subtests",
            "--plugin=nose2.plugins.junitxml",
            "--junit-xml",
            f"--junit-xml-path={self.junit_report}",
            "-v",
            "test_subtests.Case.test_subtest_failure",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertTestRunOutputMatches(proc, stderr="FAILED")
        self.assertEqual(proc.poll(), 1)

        tree = read_report(self.junit_report)
        self.assertEqual(tree.get("tests"), "1")
        self.assertEqual(tree.get("failures"), "3")
        self.assertEqual(tree.get("errors"), "0")
        self.assertEqual(tree.get("skipped"), "0")
        self.assertEqual(len(tree.findall("testcase")), 3)

        for index, test_case in enumerate(tree.findall("testcase")):
            self.assertEqual(
                test_case.get("name"),
                f"test_subtest_failure (i={index * 2 + 1})",
            )

    def test_error(self):
        proc = self.runIn(
            "scenario/subtests",
            "--plugin=nose2.plugins.junitxml",
            "--junit-xml",
            f"--junit-xml-path={self.junit_report}",
            "-v",
            "test_subtests.Case.test_subtest_error",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertTestRunOutputMatches(proc, stderr="FAILED")
        self.assertEqual(proc.poll(), 1)

        tree = read_report(self.junit_report)
        self.assertEqual(tree.get("tests"), "1")
        self.assertEqual(tree.get("failures"), "0")
        self.assertEqual(tree.get("errors"), "3")
        self.assertEqual(tree.get("skipped"), "0")
        self.assertEqual(len(tree.findall("testcase")), 3)

        for index, test_case in enumerate(tree.findall("testcase")):
            self.assertEqual(test_case.get("name"), f"test_subtest_error (i={index})")

    def test_expected_failure(self):
        proc = self.runIn(
            "scenario/subtests",
            "--plugin=nose2.plugins.junitxml",
            "--junit-xml",
            f"--junit-xml-path={self.junit_report}",
            "-v",
            "test_subtests.Case.test_subtest_expected_failure",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertTestRunOutputMatches(proc, stderr="OK")
        self.assertEqual(proc.poll(), 0)

        tree = read_report(self.junit_report)
        self.assertEqual(tree.get("tests"), "1")
        self.assertEqual(tree.get("failures"), "0")
        self.assertEqual(tree.get("errors"), "0")
        self.assertEqual(tree.get("skipped"), "1")
        self.assertEqual(len(tree.findall("testcase")), 1)

        for test_case in tree.findall("testcase"):
            self.assertEqual(test_case.get("name"), "test_subtest_expected_failure")

    def test_message(self):
        proc = self.runIn(
            "scenario/subtests",
            "--plugin=nose2.plugins.junitxml",
            "--junit-xml",
            f"--junit-xml-path={self.junit_report}",
            "-v",
            "test_subtests.Case.test_subtest_message",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertTestRunOutputMatches(proc, stderr="FAILED")
        self.assertEqual(proc.poll(), 1)

        tree = read_report(self.junit_report)
        self.assertEqual(tree.get("tests"), "1")
        self.assertEqual(tree.get("failures"), "3")
        self.assertEqual(tree.get("errors"), "0")
        self.assertEqual(tree.get("skipped"), "0")
        self.assertEqual(len(tree.findall("testcase")), 3)

        for index, test_case in enumerate(tree.findall("testcase")):
            self.assertEqual(
                test_case.get("name"),
                f"test_subtest_message [msg] (i={index * 2 + 1})",
            )

    def test_all(self):
        proc = self.runIn(
            "scenario/subtests",
            "--plugin=nose2.plugins.junitxml",
            "--junit-xml",
            f"--junit-xml-path={self.junit_report}",
            "-v",
            "test_subtests",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 5 tests")
        self.assertTestRunOutputMatches(proc, stderr="FAILED")
        self.assertEqual(proc.poll(), 1)

        tree = read_report(self.junit_report)
        self.assertEqual(tree.get("tests"), "5")
        self.assertEqual(tree.get("failures"), "6")
        self.assertEqual(tree.get("errors"), "3")
        self.assertEqual(tree.get("skipped"), "1")
        self.assertEqual(len(tree.findall("testcase")), 11)


class TestSubtestsFailFast(FunctionalTestCase):
    def test_failure(self):
        proc = self.runIn(
            "scenario/subtests", "-v", "test_subtests.Case.test_subtest_failure"
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_failure.*\(i=1\)")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_failure.*\(i=3\)")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_failure.*\(i=5\)")
        self.assertTestRunOutputMatches(proc, stderr=r"FAILED \(failures=3\)")
        self.assertEqual(proc.poll(), 1)

    def test_failfast(self):
        proc = self.runIn(
            "scenario/subtests",
            "--fail-fast",
            "-v",
            "test_subtests.Case.test_subtest_failure",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertTestRunOutputMatches(proc, stderr=r"test_subtest_failure.*\(i=1\)")
        self.assertTestRunOutputMatches(proc, stderr=r"FAILED \(failures=1\)")
        self.assertEqual(proc.poll(), 1)
