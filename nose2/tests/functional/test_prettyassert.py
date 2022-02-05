import sys

from nose2.tests._common import FunctionalTestCase, windows_ci_skip

# detect if DEBUG_RANGES are enabled in the interpreter
#
# for now, assume it's on for py3.11+
#
# in 3.11 this is be part of the env var flag loading logic:
# https://github.com/python/cpython/blob/99fcf1505218464c489d419d4500f126b6d6dc28/Python/initconfig.c#L1722-L1725
#
# if anyone runs into failures because they're setting PYTHONNODEBUGRANGES when running
# tests, we may want to look into how to pull this value from `sys` or a similar module
# note that this can be set via env var or a CLI flag
DEBUG_RANGES = sys.version_info >= (3, 11)


class TestPrettyAsserts(FunctionalTestCase):
    def assertProcOutputPattern(self, proc, expected, assert_exit_status=1):
        """
        - proc: a popen proc to check output on
        - expected: expected output pattern
        """
        stdout, stderr = proc.communicate()

        if assert_exit_status is not None:
            self.assertEqual(assert_exit_status, proc.poll())

        self.assertTestRunOutputMatches(proc, stderr=expected)

        return stderr

    def test_simple_global(self):
        proc = self.runIn(
            "scenario/pretty_asserts/simple_global", "-v", "--pretty-assert"
        )
        expected = "\n".join(
            [">>> assert myglob == 2", "", "values:", "    myglob = 1", ""]
        )
        self.assertProcOutputPattern(proc, expected)

    def test_conf_on(self):
        proc = self.runIn("scenario/pretty_asserts/conf_on", "-v")
        expected = "\n".join(
            [">>> assert myglob == 2", "", "values:", "    myglob = 1", ""]
        )
        self.assertProcOutputPattern(proc, expected)

    def test_conf_on_suppresses_clihelp(self):
        proc = self.runIn("scenario/pretty_asserts/conf_on", "--help")
        stdout, stderr = proc.communicate()
        exit_status = proc.poll()
        assert "--pretty-assert" not in stdout
        assert "--pretty-assert" not in stderr
        assert exit_status == 0

    def test_conf_on_plus_arg(self):
        """ensures that #432 stays fixed"""
        proc = self.runIn("scenario/pretty_asserts/conf_on", "-v", "--pretty-assert")
        expected = "\n".join(
            [">>> assert myglob == 2", "", "values:", "    myglob = 1", ""]
        )
        self.assertProcOutputPattern(proc, expected)

    def test_assign_after_assert(self):
        proc = self.runIn(
            "scenario/pretty_asserts/assign_after_assert", "-v", "--pretty-assert"
        )
        expected = "\n".join([">>> assert x == 2", "", "values:", "    x = 1", ""])
        self.assertProcOutputPattern(proc, expected)

    def test_multiline_assert_statement(self):
        proc = self.runIn(
            "scenario/pretty_asserts/multiline_statement", "-v", "--pretty-assert"
        )
        expected = "\n".join(
            [
                ">>> assert \\(x",
                ">>>         >",
                '>>>         y\\), \\"oh noez, x <= y\\"',
                "",
                "message:",
                "    oh noez, x <= y",
                "",
                "values:",
                "    x = 1",
                "    y = 2",
                "",
            ]
        )
        self.assertProcOutputPattern(proc, expected)

    def test_multiline_funcdef(self):
        proc = self.runIn(
            "scenario/pretty_asserts/multiline_funcdef", "--pretty-assert"
        )
        expected1 = "\n".join(
            [
                '>>> assert x > y, \\"oh noez, x <= y\\"',
                "",
                "message:",
                "    oh noez, x <= y",
                "",
                "values:",
                "    x = 1",
                "    y = 2",
                "",
            ]
        )
        expected2 = "\n".join(
            [">>> assert not value", "", "values:", "    value = 'foo'", ""]
        )
        expected3 = "\n".join(
            [">>> assert not value", "", "values:", "    value = 'bar'", ""]
        )
        self.assertProcOutputPattern(proc, expected1)
        self.assertProcOutputPattern(proc, expected2)
        self.assertProcOutputPattern(proc, expected3)

    def test_assert_attribute_resolution(self):
        proc = self.runIn(
            "scenario/pretty_asserts/attribute_resolution", "-v", "--pretty-assert"
        )
        expected = "\n".join(
            [
                ">>> assert x.x \\!= \\(self",
                ">>>                \\).x",
                "",
                "values:",
                (
                    "    x = <test_prettyassert_attribute_resolution.TestFoo"
                    " testMethod=test_ohnoez>"
                ),
                "    x.x = 1",
                (
                    "    self = <test_prettyassert_attribute_resolution.TestFoo"
                    " testMethod=test_ohnoez>"
                ),
                "",
            ]
        )
        self.assertProcOutputPattern(proc, expected)

    @windows_ci_skip
    def test_assert_attribute_resolution2(self):
        proc = self.runIn(
            "scenario/pretty_asserts/attribute_resolution2", "-v", "--pretty-assert"
        )
        expected = "\n".join(
            [
                ">>> assert foo\\(\\).x \\!= self.x",
                "",
                "values:",
                (
                    "    foo = <function (TestFoo.test_ohnoez.<locals>.|)foo at "
                    "0x[a-z0-9]+>"
                ),
                (
                    "    self = <test_prettyassert_attribute_resolution2.TestFoo"
                    " testMethod=test_ohnoez>"
                ),
                "    self.x = 1",
                "",
            ]
        )
        self.assertProcOutputPattern(proc, expected)

    def test_assert_ignore_passing(self):
        proc = self.runIn(
            "scenario/pretty_asserts/ignore_passing", "-v", "--pretty-assert"
        )
        expected1 = "\n".join(
            [">>> assert x; assert y", "", "values:", "    y = False", ""]
        )
        expected2 = "\n".join([">>> assert q", "", "values:", "    q = 0", ""])
        self.assertProcOutputPattern(proc, expected1)
        self.assertProcOutputPattern(proc, expected2)

    def test_unittest_assertion(self):
        proc = self.runIn(
            "scenario/pretty_asserts/unittest_assertion", "-v", "--pretty-assert"
        )
        # look for typical unittest output
        expect_lines = [
            r"self.assertTrue\(x\)",
            r"\s+\^+",
            "AssertionError: False is not true",
        ]
        if not DEBUG_RANGES:
            del expect_lines[1]
        expected = "\n".join(expect_lines)
        stderr = self.assertProcOutputPattern(proc, expected)
        # the assertion line wasn't reprinted by prettyassert
        self.assertNotIn(">>> self.assertTrue", stderr)
        # the assertion values weren't printed by prettyassert
        self.assertNotIn("values:", stderr)
