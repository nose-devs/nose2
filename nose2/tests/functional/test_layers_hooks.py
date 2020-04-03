import os
import sys

from nose2.tests._common import FunctionalTestCase


class TestLayerHooks(FunctionalTestCase):
    @classmethod
    def setUp(cls):
        filepath = os.path.dirname(os.path.realpath(__file__))
        cls.libpath = os.path.join(filepath, "support", "lib")
        sys.path.append(cls.libpath)

    @classmethod
    def tearDown(cls):
        if cls.libpath in sys.path:
            sys.path.remove(cls.libpath)

    def test_simple_such(self):
        proc = self.runIn(
            "scenario/layers_hooks",
            "--plugin=nose2.plugins.layers",
            "--plugin=layer_hooks_plugin",
            "test_simple_such",
        )
        expected = r"""^StartLayerSetup: <class 'test_simple_such.A system:layer'>
StopLayerSetup: <class 'test_simple_such.A system:layer'>
StartLayerSetupTest: <class 'test_simple_such.A system:layer'>:test 0000: should do something \(test_simple_such.A system\)
StopLayerSetupTest: <class 'test_simple_such.A system:layer'>:test 0000: should do something \(test_simple_such.A system\)
StartLayerTeardownTest: <class 'test_simple_such.A system:layer'>:test 0000: should do something \(test_simple_such.A system\)
StopLayerTeardownTest: <class 'test_simple_such.A system:layer'>:test 0000: should do something \(test_simple_such.A system\)
StartLayerTeardown: <class 'test_simple_such.A system:layer'>
StopLayerTeardown: <class 'test_simple_such.A system:layer'>\n*$"""  # noqa: E501
        self.assertTestRunOutputMatches(proc, stderr="Ran 1 test")
        self.assertTestRunOutputMatches(proc, stdout=expected)
        self.assertEqual(proc.poll(), 0, proc.stderr.getvalue())

    def test_complex_such(self):
        proc = self.runIn(
            "such/",
            "--plugin=nose2.plugins.layers",
            "--plugin=layer_hooks_plugin",
            "test_such",
        )
        expected = r"""StartLayerSetup: <class 'test_such.A system with complex setup:layer'>
StopLayerSetup: <class 'test_such.A system with complex setup:layer'>
StartLayerSetupTest: <class 'test_such.A system with complex setup:layer'>:test 0000: should do something \(test_such.A system with complex setup\)
StopLayerSetupTest: <class 'test_such.A system with complex setup:layer'>:test 0000: should do something \(test_such.A system with complex setup\)
StartLayerTeardownTest: <class 'test_such.A system with complex setup:layer'>:test 0000: should do something \(test_such.A system with complex setup\)
StopLayerTeardownTest: <class 'test_such.A system with complex setup:layer'>:test 0000: should do something \(test_such.A system with complex setup\)
StartLayerSetup: <class 'test_such.having an expensive fixture:layer'>
StopLayerSetup: <class 'test_such.having an expensive fixture:layer'>
StartLayerSetupTest: <class 'test_such.having an expensive fixture:layer'>:test 0000: should do more things \(test_such.having an expensive fixture\)
StopLayerSetupTest: <class 'test_such.having an expensive fixture:layer'>:test 0000: should do more things \(test_such.having an expensive fixture\)
StartLayerTeardownTest: <class 'test_such.having an expensive fixture:layer'>:test 0000: should do more things \(test_such.having an expensive fixture\)
StopLayerTeardownTest: <class 'test_such.having an expensive fixture:layer'>:test 0000: should do more things \(test_such.having an expensive fixture\)
StartLayerSetup: <class 'test_such.having another precondtion:layer'>
StopLayerSetup: <class 'test_such.having another precondtion:layer'>
StartLayerSetupTest: <class 'test_such.having another precondtion:layer'>:test 0000: should do that not this \(test_such.having another precondtion\)
StopLayerSetupTest: <class 'test_such.having another precondtion:layer'>:test 0000: should do that not this \(test_such.having another precondtion\)
StartLayerTeardownTest: <class 'test_such.having another precondtion:layer'>:test 0000: should do that not this \(test_such.having another precondtion\)
StopLayerTeardownTest: <class 'test_such.having another precondtion:layer'>:test 0000: should do that not this \(test_such.having another precondtion\)
StartLayerSetupTest: <class 'test_such.having another precondtion:layer'>:test 0001: should do this not that \(test_such.having another precondtion\)
StopLayerSetupTest: <class 'test_such.having another precondtion:layer'>:test 0001: should do this not that \(test_such.having another precondtion\)
StartLayerTeardownTest: <class 'test_such.having another precondtion:layer'>:test 0001: should do this not that \(test_such.having another precondtion\)
StopLayerTeardownTest: <class 'test_such.having another precondtion:layer'>:test 0001: should do this not that \(test_such.having another precondtion\)
StartLayerTeardown: <class 'test_such.having another precondtion:layer'>
StopLayerTeardown: <class 'test_such.having another precondtion:layer'>
StartLayerSetup: <class 'test_such.SomeLayer'>
StopLayerSetup: <class 'test_such.SomeLayer'>
StartLayerSetup: <class 'test_such.having a different precondition:layer'>
StopLayerSetup: <class 'test_such.having a different precondition:layer'>
StartLayerSetupTest: <class 'test_such.having a different precondition:layer'>:test 0000: should do something else \(test_such.having a different precondition\)
StopLayerSetupTest: <class 'test_such.having a different precondition:layer'>:test 0000: should do something else \(test_such.having a different precondition\)
StartLayerTeardownTest: <class 'test_such.having a different precondition:layer'>:test 0000: should do something else \(test_such.having a different precondition\)
StopLayerTeardownTest: <class 'test_such.having a different precondition:layer'>:test 0000: should do something else \(test_such.having a different precondition\)
StartLayerSetupTest: <class 'test_such.having a different precondition:layer'>:test 0001: should have another test \(test_such.having a different precondition\)
StopLayerSetupTest: <class 'test_such.having a different precondition:layer'>:test 0001: should have another test \(test_such.having a different precondition\)
StartLayerTeardownTest: <class 'test_such.having a different precondition:layer'>:test 0001: should have another test \(test_such.having a different precondition\)
StopLayerTeardownTest: <class 'test_such.having a different precondition:layer'>:test 0001: should have another test \(test_such.having a different precondition\)
StartLayerSetupTest: <class 'test_such.having a different precondition:layer'>:test 0002: should have access to an external fixture \(test_such.having a different precondition\)
StopLayerSetupTest: <class 'test_such.having a different precondition:layer'>:test 0002: should have access to an external fixture \(test_such.having a different precondition\)
StartLayerTeardownTest: <class 'test_such.having a different precondition:layer'>:test 0002: should have access to an external fixture \(test_such.having a different precondition\)
StopLayerTeardownTest: <class 'test_such.having a different precondition:layer'>:test 0002: should have access to an external fixture \(test_such.having a different precondition\)
StartLayerSetup: <class 'test_such.having a case inside the external fixture:layer'>
StopLayerSetup: <class 'test_such.having a case inside the external fixture:layer'>
StartLayerSetupTest: <class 'test_such.having a case inside the external fixture:layer'>:test 0000: should still have access to that fixture \(test_such.having a case inside the external fixture\)
StopLayerSetupTest: <class 'test_such.having a case inside the external fixture:layer'>:test 0000: should still have access to that fixture \(test_such.having a case inside the external fixture\)
StartLayerTeardownTest: <class 'test_such.having a case inside the external fixture:layer'>:test 0000: should still have access to that fixture \(test_such.having a case inside the external fixture\)
StopLayerTeardownTest: <class 'test_such.having a case inside the external fixture:layer'>:test 0000: should still have access to that fixture \(test_such.having a case inside the external fixture\)
StartLayerTeardown: <class 'test_such.having a case inside the external fixture:layer'>
StopLayerTeardown: <class 'test_such.having a case inside the external fixture:layer'>
StartLayerTeardown: <class 'test_such.having a different precondition:layer'>
StopLayerTeardown: <class 'test_such.having a different precondition:layer'>
StartLayerTeardown: <class 'test_such.SomeLayer'>
StopLayerTeardown: <class 'test_such.SomeLayer'>
StartLayerTeardown: <class 'test_such.having an expensive fixture:layer'>
StopLayerTeardown: <class 'test_such.having an expensive fixture:layer'>
StartLayerTeardown: <class 'test_such.A system with complex setup:layer'>
StopLayerTeardown: <class 'test_such.A system with complex setup:layer'>\n*$"""  # noqa: E501
        self.assertTestRunOutputMatches(proc, stderr="Ran 9 tests")
        self.assertTestRunOutputMatches(proc, stdout=expected)
        self.assertEqual(proc.poll(), 0, proc.stderr.getvalue())

    def test_simple_layers(self):
        proc = self.runIn(
            "scenario/layers_hooks",
            "--plugin=nose2.plugins.layers",
            "--plugin=layer_hooks_plugin",
            "test_layers_simple",
        )
        expected = r"""^StartLayerSetup: <class 'test_layers_simple.Layer1'>
StopLayerSetup: <class 'test_layers_simple.Layer1'>
StartLayerSetupTest: <class 'test_layers_simple.Layer1'>:test_1 \(test_layers_simple.TestSimple\)
StopLayerSetupTest: <class 'test_layers_simple.Layer1'>:test_1 \(test_layers_simple.TestSimple\)
StartLayerTeardownTest: <class 'test_layers_simple.Layer1'>:test_1 \(test_layers_simple.TestSimple\)
StopLayerTeardownTest: <class 'test_layers_simple.Layer1'>:test_1 \(test_layers_simple.TestSimple\)
StartLayerSetupTest: <class 'test_layers_simple.Layer1'>:test_2 \(test_layers_simple.TestSimple\)
StopLayerSetupTest: <class 'test_layers_simple.Layer1'>:test_2 \(test_layers_simple.TestSimple\)
StartLayerTeardownTest: <class 'test_layers_simple.Layer1'>:test_2 \(test_layers_simple.TestSimple\)
StopLayerTeardownTest: <class 'test_layers_simple.Layer1'>:test_2 \(test_layers_simple.TestSimple\)
StartLayerTeardown: <class 'test_layers_simple.Layer1'>
StopLayerTeardown: <class 'test_layers_simple.Layer1'>\n*$"""  # noqa: E501
        self.assertTestRunOutputMatches(proc, stderr="Ran 2 tests")
        self.assertTestRunOutputMatches(proc, stdout=expected)
        self.assertEqual(proc.poll(), 0, proc.stderr.getvalue())
