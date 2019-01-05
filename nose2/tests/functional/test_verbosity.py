from nose2.tests._common import FunctionalTestCase

_SUFFIX = (
    "\n----------------------------------------------------------------------"
    "\nRan 1 test "
)

Q_TEST_PATTERN = r"(?<!\.)(?<!ok)" + _SUFFIX
MID_TEST_PATTERN = r"\." + _SUFFIX
V_TEST_PATTERN = r"test \(__main__\.Test\) \.\.\. ok" + "\n" + _SUFFIX


class TestVerbosity(FunctionalTestCase):
    def test_no_modifier(self):
        proc = self.runModuleAsMain("scenario/one_test/tests.py")
        self.assertTestRunOutputMatches(proc, stderr=MID_TEST_PATTERN)

    def test_one_v(self):
        proc = self.runModuleAsMain("scenario/one_test/tests.py", "-v")
        self.assertTestRunOutputMatches(proc, stderr=V_TEST_PATTERN)

    def test_one_q(self):
        proc = self.runModuleAsMain("scenario/one_test/tests.py", "-q")
        self.assertTestRunOutputMatches(proc, stderr=Q_TEST_PATTERN)

    def test_one_q_one_v(self):
        proc = self.runModuleAsMain("scenario/one_test/tests.py", "-q", "-v")
        self.assertTestRunOutputMatches(proc, stderr=MID_TEST_PATTERN)

        proc = self.runModuleAsMain("scenario/one_test/tests.py", "-qv")
        self.assertTestRunOutputMatches(proc, stderr=MID_TEST_PATTERN)

    def test_one_q_two_vs(self):
        proc = self.runModuleAsMain("scenario/one_test/tests.py", "-q", "-v", "-v")
        self.assertTestRunOutputMatches(proc, stderr=V_TEST_PATTERN)

        proc = self.runModuleAsMain("scenario/one_test/tests.py", "-qvv")
        self.assertTestRunOutputMatches(proc, stderr=V_TEST_PATTERN)

    def test_one_v_two_qs(self):
        proc = self.runModuleAsMain("scenario/one_test/tests.py", "-v", "-q", "-q")
        self.assertTestRunOutputMatches(proc, stderr=Q_TEST_PATTERN)

        proc = self.runModuleAsMain("scenario/one_test/tests.py", "-vqq")
        self.assertTestRunOutputMatches(proc, stderr=Q_TEST_PATTERN)

    def test_explicit_verbosity(self):
        proc = self.runModuleAsMain("scenario/one_test/tests.py", "--verbosity", "0")
        self.assertTestRunOutputMatches(proc, stderr=Q_TEST_PATTERN)

        proc = self.runModuleAsMain("scenario/one_test/tests.py", "--verbosity", "1")
        self.assertTestRunOutputMatches(proc, stderr=MID_TEST_PATTERN)

        proc = self.runModuleAsMain("scenario/one_test/tests.py", "--verbosity", "2")
        self.assertTestRunOutputMatches(proc, stderr=V_TEST_PATTERN)

        proc = self.runModuleAsMain("scenario/one_test/tests.py", "--verbosity", "-1")
        self.assertTestRunOutputMatches(proc, stderr=Q_TEST_PATTERN)

    def test_tweaked_explicit_verbosity(self):
        proc = self.runModuleAsMain(
            "scenario/one_test/tests.py", "--verbosity", "0", "-vv"
        )
        self.assertTestRunOutputMatches(proc, stderr=V_TEST_PATTERN)
        proc = self.runModuleAsMain(
            "scenario/one_test/tests.py", "-vv", "--verbosity", "0"
        )
        self.assertTestRunOutputMatches(proc, stderr=V_TEST_PATTERN)

        proc = self.runModuleAsMain(
            "scenario/one_test/tests.py", "--verbosity", "2", "-q"
        )
        self.assertTestRunOutputMatches(proc, stderr=MID_TEST_PATTERN)
        proc = self.runModuleAsMain(
            "scenario/one_test/tests.py", "-q", "--verbosity", "2", "-q"
        )
        self.assertTestRunOutputMatches(proc, stderr=Q_TEST_PATTERN)
