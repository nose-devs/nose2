from nose2.tests._common import FunctionalTestCase


class TestPrettyAsserts(FunctionalTestCase):
    def assertProcOutputPattern(self, proc, expected, assert_exit_status=1):
        """
        - proc: a popen proc to check output on
        - expected: expected output pattern
        """
        stdout, stderr = proc.communicate()

        if assert_exit_status is not None:
            self.assertEqual(assert_exit_status, proc.poll())

        self.assertTestRunOutputMatches(
            proc,
            stderr=expected)

    def test_simple_global(self):
        proc = self.runIn(
            'scenario/pretty_asserts/simple_global',
            '-v', '--pretty-assert',
        )
        expected = "\n".join([
            ">>> assert myglob == 2",
            "",
            "values:",
            "    myglob = 1",
            ""
        ])
        self.assertProcOutputPattern(proc, expected)

    def test_conf_on(self):
        proc = self.runIn(
            'scenario/pretty_asserts/conf_on',
            '-v',
        )
        expected = "\n".join([
            ">>> assert myglob == 2",
            "",
            "values:",
            "    myglob = 1",
            ""
        ])
        self.assertProcOutputPattern(proc, expected)

    def test_assign_after_assert(self):
        proc = self.runIn(
            'scenario/pretty_asserts/assign_after_assert',
            '-v', '--pretty-assert',
        )
        expected = "\n".join([
            ">>> assert x == 2",
            "",
            "values:",
            "    x = 1",
            ""
        ])
        self.assertProcOutputPattern(proc, expected)

    def test_multiline_assert_statement(self):
        proc = self.runIn(
            'scenario/pretty_asserts/multiline_statement',
            '-v', '--pretty-assert',
        )
        expected = "\n".join([
            '>>> assert \\(x',
            '>>>         >',
            '>>>         y\\), \\"oh noez, x <= y\\"',
            '',
            'message:',
            '    oh noez, x <= y',
            '',
            'values:',
            '    x = 1',
            '    y = 2',
            ''
        ])
        self.assertProcOutputPattern(proc, expected)

    def test_assert_attribute_resolution(self):
        proc = self.runIn(
            'scenario/pretty_asserts/attribute_resolution',
            '-v', '--pretty-assert',
        )
        expected = "\n".join([
            ">>> assert x.x \\!= \\(self",
            ">>>                \\).x",
            "",
            "values:",
            ("    x = <test_prettyassert_attribute_resolution.TestFoo"
             " testMethod=test_ohnoez>"),
            "    x.x = 1",
            ("    self = <test_prettyassert_attribute_resolution.TestFoo"
             " testMethod=test_ohnoez>"),
            "",
        ])
        self.assertProcOutputPattern(proc, expected)
