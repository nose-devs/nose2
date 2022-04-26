from nose2.tests._common import FunctionalTestCase, _method_name


class TestLayers(FunctionalTestCase):
    def test_runs_layer_fixtures(self):
        proc = self.runIn("scenario/layers", "-v", "--plugin=nose2.plugins.layers")
        self.assertTestRunOutputMatches(proc, stderr="Ran 8 tests")
        self.assertEqual(proc.poll(), 0)

    def test_scenario_fails_without_plugin(self):
        proc = self.runIn("scenario/layers", "-v")
        self.assertTestRunOutputMatches(proc, stderr="Ran 8 tests")
        self.assertTestRunOutputMatches(proc, stderr=r"FAILED \(failures=7\)")
        self.assertEqual(proc.poll(), 1)

    def test_methods_run_once_per_class(self):
        proc = self.runIn(
            "scenario/layers_with_inheritance", "-v", "--plugin=nose2.plugins.layers"
        )

        expected = (
            "^"
            "L1 setUp\n"
            "L2 setUp\n"
            "L1 testSetUp\n"
            "L2 testSetUp\n"
            "Run test1\n"
            "L2 testTearDown\n"
            "L1 testTearDown\n"
            "L1 testSetUp\n"
            "L2 testSetUp\n"
            "Run test2\n"
            "L2 testTearDown\n"
            "L1 testTearDown\n"
            "L1 tearDown\n"
            "$"
        )
        self.assertTestRunOutputMatches(proc, stdout=expected)
        self.assertEqual(proc.poll(), 0)

    def test_layer_reporter_output(self):
        proc = self.runIn(
            "scenario/layers", "-v", "--plugin=nose2.plugins.layers", "--layer-reporter"
        )
        expect = (
            r"""test \(test_layers.NoLayer"""
            + _method_name()
            + r"""\) ... ok
Base
  test \(test_layers.Outer"""
            + _method_name()
            + r"""\) ... ok
  LayerD
    test \(test_layers.InnerD"""
            + _method_name()
            + r"""\) test with docstring ... ok
  LayerA
    test \(test_layers.InnerA"""
            + _method_name()
            + r"""\) ... ok
  LayerB
    LayerB_1
      test \(test_layers.InnerB_1"""
            + _method_name()
            + r"""\) ... ok
    LayerC
      test \(test_layers.InnerC"""
            + _method_name()
            + r"""\) ... ok
      test2 \(test_layers.InnerC"""
            + _method_name("test2")
            + r"""\) ... ok
    LayerA_1
      test \(test_layers.InnerA_1"""
            + _method_name()
            + r"""\) ... ok"""
        ).split("\n")
        self.assertTestRunOutputMatches(proc, stderr="Ran 8 tests")
        for line in expect:
            self.assertTestRunOutputMatches(proc, stderr=line)
        self.assertEqual(proc.poll(), 0)

    def test_layer_reporter_error_output(self):
        proc = self.runIn(
            "scenario/layers_with_errors",
            "--plugin=nose2.plugins.layers",
            "--layer-reporter",
        )
        expect = [
            r"ERROR: fixture with a value test_err \(test_layers_with_errors.Test"
            + _method_name("test_err")
            + r"\)",
            "ERROR: A test scenario with errors should check for an attribute "
            "that does not exist and raise an error",
            r"FAIL: fixture with a value test_fail \(test_layers_with_errors.Test"
            + _method_name("test_fail")
            + r"\)",
            "FAIL: A test scenario with errors should check that value == 2 "
            "and fail",
        ]
        for line in expect:
            self.assertTestRunOutputMatches(proc, stderr=line)
        self.assertEqual(proc.poll(), 1)

    def test_layers_and_attributes(self):
        proc = self.runIn(
            "scenario/layers_and_attributes",
            "-v",
            "--plugin=nose2.plugins.attrib",
            "--plugin=nose2.plugins.layers",
            "-A",
            "a=1",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertEqual(proc.poll(), 0)

    def test_teardown_fail(self):
        proc = self.runIn(
            "scenario/layers_with_errors",
            "--plugin=nose2.plugins.layers",
            "-v",
            "test_layer_teardown_fail",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test in")
        self.assertTestRunOutputMatches(proc, stderr="ERROR: LayerSuite")
        self.assertTestRunOutputMatches(proc, stderr="FAIL")
        self.assertTestRunOutputMatches(proc, stderr="Bad Error in Layer testTearDown")

    def test_setup_fail(self):
        proc = self.runIn(
            "scenario/layers_with_errors",
            "--plugin=nose2.plugins.layers",
            "-v",
            "test_layer_setup_fail",
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 0 tests in")
        self.assertTestRunOutputMatches(proc, stderr="ERROR: LayerSuite")
        self.assertTestRunOutputMatches(proc, stderr="FAIL")
        self.assertTestRunOutputMatches(proc, stderr="Bad Error in Layer setUp!")

    def test_layers_and_non_layers(self):
        proc = self.runIn(
            "scenario/", "layers_and_non_layers", "-v", "--plugin=nose2.plugins.layers"
        )
        self.assertTestRunOutputMatches(proc, stderr="Ran 12 tests in")
        self.assertTestRunOutputMatches(proc, stderr="OK")
        self.assertEqual(proc.poll(), 0)
