from nose2.tests._common import FunctionalTestCase, support_file


class TestDoctestsPlugin(FunctionalTestCase):
    def test_simple(self):
        proc = self.runIn(
            "scenario/doctests",
            "-v",
            "--plugin=nose2.plugins.doctests",
            "--with-doctest",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 6 tests")
        self.assertTestRunOutputMatches(proc, stderr="Doctest: docs ... ok")
        self.assertTestRunOutputMatches(proc, stderr="Doctest: docs.rst ... ok")
        self.assertTestRunOutputMatches(proc, stderr="Doctest: docs.txt ... ok")
        self.assertTestRunOutputMatches(
            proc, stderr="Doctest: doctests_pkg1.docs1 ... ok"
        )
        self.assertTestRunOutputMatches(proc, stderr="Doctest: docs1.rst ... ok")
        self.assertTestRunOutputMatches(proc, stderr="Doctest: docs1.txt ... ok")
        self.assertEqual(proc.poll(), 0)

    def test_start_directory_inside_package(self):
        proc = self.runIn(
            "scenario/doctests/doctests_pkg1",
            "-v",
            "--plugin=nose2.plugins.doctests",
            "--with-doctest",
            "-t",
            support_file("scenario/doctests"),
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 3 tests")
        self.assertTestRunOutputMatches(
            proc, stderr="Doctest: doctests_pkg1.docs1 ... ok"
        )
        self.assertTestRunOutputMatches(proc, stderr="Doctest: docs1.rst ... ok")
        self.assertTestRunOutputMatches(proc, stderr="Doctest: docs1.txt ... ok")
        self.assertEqual(proc.poll(), 0)

    def test_project_directory_inside_package(self):
        proc = self.runIn(
            "scenario/doctests/doctests_pkg1",
            "-v",
            "--plugin=nose2.plugins.doctests",
            "--with-doctest",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 3 tests")
        self.assertTestRunOutputMatches(
            proc, stderr="Doctest: doctests_pkg1.docs1 ... ok"
        )
        self.assertTestRunOutputMatches(proc, stderr="Doctest: docs1.rst ... ok")
        self.assertTestRunOutputMatches(proc, stderr="Doctest: docs1.txt ... ok")
        self.assertEqual(proc.poll(), 0)
