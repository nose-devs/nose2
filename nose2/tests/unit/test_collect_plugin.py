import re
import unittest2

from ._common import FunctionalTestCase, FakeStartTestRunEvent
from ..plugins import collect


class CollectOnlyFunctionalTest(FunctionalTestCase):
    def test_layout1(self):
        self.assertTestRunOutputMatches(
            self.runIn('layout1', '-v', '--collect-only'),
            stderr=EXPECT_LAYOUT1)


class TestCollectOnly(unittest2.TestCase):
    tags = ['unit']

    def setUp(self):
        self.plugin = collect.CollectOnly()

    def test_startTestRun_sets_executeTests(self):
        event = FakeStartTestRunEvent()
        self.plugin.startTestRun(event)
        self.assertEqual(event.executeTests, self.plugin.collectTests)


# expectations

EXPECT_LAYOUT1 = re.compile("""\
test_failed \(pkg1\.test\.test_things\.SomeTests\) \.\.\. ok
test_ok \(pkg1\.test\.test_things\.SomeTests\) \.\.\. ok
test_skippy \(pkg1\.test\.test_things\.SomeTests\) \.\.\. ok
test_typeerr \(pkg1\.test\.test_things\.SomeTests\) \.\.\. ok
unittest2\.case\.FunctionTestCase \(test_fixt\) \.\.\. ok
unittest2\.case\.FunctionTestCase \(test_func\) \.\.\. ok
pkg1\.test\.test_things\.test_gen:1
0, 0 \.\.\. ok
pkg1\.test\.test_things\.test_gen:2
1, 1 \.\.\. ok
pkg1\.test\.test_things\.test_gen:3
2, 2 \.\.\. ok
pkg1\.test\.test_things\.test_gen:4
3, 3 \.\.\. ok
pkg1\.test\.test_things\.test_gen:5
4, 4 \.\.\. ok
pkg1\.test\.test_things\.test_gen_nose_style:1
0, 0 \.\.\. ok
pkg1\.test\.test_things\.test_gen_nose_style:2
1, 1 \.\.\. ok
pkg1\.test\.test_things\.test_gen_nose_style:3
2, 2 \.\.\. ok
pkg1\.test\.test_things\.test_gen_nose_style:4
3, 3 \.\.\. ok
pkg1\.test\.test_things\.test_gen_nose_style:5
4, 4 \.\.\. ok

----------------------------------------------------------------------
Ran 16 tests in \d.\d+s

OK
""")
