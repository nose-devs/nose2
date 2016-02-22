import sys
import os
from nose2.tests._common import FunctionalTestCase


class TestLayerHooks(FunctionalTestCase):

    @classmethod
    def setUp(cls):
        filepath = os.path.dirname(os.path.realpath(__file__))
        cls.libpath = os.path.join(filepath, 'support', 'lib')
        sys.path.append(cls.libpath)

    @classmethod
    def tearDown(cls):
        if cls.libpath in sys.path:
            sys.path.remove(cls.libpath)

    def test_simple_such(self):
        proc = self.runIn(
            'scenario/layers_hooks',
            '--plugin=nose2.plugins.layers',
            '--plugin=layer_hooks_plugin',
            'test_simple_such')
        expected = (
            "^"
            "StartLayerSetup: <class 'test_simple_such.A system:layer'>\n"
            "StopLayerSetup: <class 'test_simple_such.A system:layer'>\n"
            "StartLayerSetupTest: <class 'test_simple_such.A system:layer'>:test 0000: should do something \(test_simple_such.A system\)\n"
            "StopLayerSetupTest: <class 'test_simple_such.A system:layer'>:test 0000: should do something \(test_simple_such.A system\)\n"
            "StartLayerTeardownTest: <class 'test_simple_such.A system:layer'>:test 0000: should do something \(test_simple_such.A system\)\n"
            "StopLayerTeardownTest: <class 'test_simple_such.A system:layer'>:test 0000: should do something \(test_simple_such.A system\)\n"
            "StartLayerTeardown: <class 'test_simple_such.A system:layer'>\n"
            "StopLayerTeardown: <class 'test_simple_such.A system:layer'>\n*"
            "$")
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertTestRunOutputMatches(proc, stdout=expected)
        self.assertEqual(proc.poll(), 0, proc.stderr.getvalue())

    def test_complex_such(self):
        proc = self.runIn(
            'such/',
            '--plugin=nose2.plugins.layers',
            '--plugin=layer_hooks_plugin',
            'test_such')
        expected = (
            "StartLayerSetup: <class 'test_such.A system with complex setup:layer'>\n"
            "StopLayerSetup: <class 'test_such.A system with complex setup:layer'>\n"
            "StartLayerSetupTest: <class 'test_such.A system with complex setup:layer'>:test 0000: should do something \(test_such.A system with complex setup\)\n"
            "StopLayerSetupTest: <class 'test_such.A system with complex setup:layer'>:test 0000: should do something \(test_such.A system with complex setup\)\n"
            "StartLayerTeardownTest: <class 'test_such.A system with complex setup:layer'>:test 0000: should do something \(test_such.A system with complex setup\)\n"
            "StopLayerTeardownTest: <class 'test_such.A system with complex setup:layer'>:test 0000: should do something \(test_such.A system with complex setup\)\n"
            "StartLayerSetup: <class 'test_such.having an expensive fixture:layer'>\n"
            "StopLayerSetup: <class 'test_such.having an expensive fixture:layer'>\n"
            "StartLayerSetupTest: <class 'test_such.having an expensive fixture:layer'>:test 0000: should do more things \(test_such.having an expensive fixture\)\n"
            "StopLayerSetupTest: <class 'test_such.having an expensive fixture:layer'>:test 0000: should do more things \(test_such.having an expensive fixture\)\n"
            "StartLayerTeardownTest: <class 'test_such.having an expensive fixture:layer'>:test 0000: should do more things \(test_such.having an expensive fixture\)\n"
            "StopLayerTeardownTest: <class 'test_such.having an expensive fixture:layer'>:test 0000: should do more things \(test_such.having an expensive fixture\)\n"
            "StartLayerSetup: <class 'test_such.having another precondtion:layer'>\n"
            "StopLayerSetup: <class 'test_such.having another precondtion:layer'>\n"
            "StartLayerSetupTest: <class 'test_such.having another precondtion:layer'>:test 0000: should do that not this \(test_such.having another precondtion\)\n"
            "StopLayerSetupTest: <class 'test_such.having another precondtion:layer'>:test 0000: should do that not this \(test_such.having another precondtion\)\n"
            "StartLayerTeardownTest: <class 'test_such.having another precondtion:layer'>:test 0000: should do that not this \(test_such.having another precondtion\)\n"
            "StopLayerTeardownTest: <class 'test_such.having another precondtion:layer'>:test 0000: should do that not this \(test_such.having another precondtion\)\n"
            "StartLayerSetupTest: <class 'test_such.having another precondtion:layer'>:test 0001: should do this not that \(test_such.having another precondtion\)\n"
            "StopLayerSetupTest: <class 'test_such.having another precondtion:layer'>:test 0001: should do this not that \(test_such.having another precondtion\)\n"
            "StartLayerTeardownTest: <class 'test_such.having another precondtion:layer'>:test 0001: should do this not that \(test_such.having another precondtion\)\n"
            "StopLayerTeardownTest: <class 'test_such.having another precondtion:layer'>:test 0001: should do this not that \(test_such.having another precondtion\)\n"
            "StartLayerTeardown: <class 'test_such.having another precondtion:layer'>\n"
            "StopLayerTeardown: <class 'test_such.having another precondtion:layer'>\n"
            "StartLayerSetup: <class 'test_such.SomeLayer'>\n"
            "StopLayerSetup: <class 'test_such.SomeLayer'>\n"
            "StartLayerSetup: <class 'test_such.having a different precondition:layer'>\n"
            "StopLayerSetup: <class 'test_such.having a different precondition:layer'>\n"
            "StartLayerSetupTest: <class 'test_such.having a different precondition:layer'>:test 0000: should do something else \(test_such.having a different precondition\)\n"
            "StopLayerSetupTest: <class 'test_such.having a different precondition:layer'>:test 0000: should do something else \(test_such.having a different precondition\)\n"
            "StartLayerTeardownTest: <class 'test_such.having a different precondition:layer'>:test 0000: should do something else \(test_such.having a different precondition\)\n"
            "StopLayerTeardownTest: <class 'test_such.having a different precondition:layer'>:test 0000: should do something else \(test_such.having a different precondition\)\n"
            "StartLayerSetupTest: <class 'test_such.having a different precondition:layer'>:test 0001: should have another test \(test_such.having a different precondition\)\n"
            "StopLayerSetupTest: <class 'test_such.having a different precondition:layer'>:test 0001: should have another test \(test_such.having a different precondition\)\n"
            "StartLayerTeardownTest: <class 'test_such.having a different precondition:layer'>:test 0001: should have another test \(test_such.having a different precondition\)\n"
            "StopLayerTeardownTest: <class 'test_such.having a different precondition:layer'>:test 0001: should have another test \(test_such.having a different precondition\)\n"
            "StartLayerSetupTest: <class 'test_such.having a different precondition:layer'>:test 0002: should have access to an external fixture \(test_such.having a different precondition\)\n"
            "StopLayerSetupTest: <class 'test_such.having a different precondition:layer'>:test 0002: should have access to an external fixture \(test_such.having a different precondition\)\n"
            "StartLayerTeardownTest: <class 'test_such.having a different precondition:layer'>:test 0002: should have access to an external fixture \(test_such.having a different precondition\)\n"
            "StopLayerTeardownTest: <class 'test_such.having a different precondition:layer'>:test 0002: should have access to an external fixture \(test_such.having a different precondition\)\n"
            "StartLayerSetup: <class 'test_such.having a case inside the external fixture:layer'>\n"
            "StopLayerSetup: <class 'test_such.having a case inside the external fixture:layer'>\n"
            "StartLayerSetupTest: <class 'test_such.having a case inside the external fixture:layer'>:test 0000: should still have access to that fixture \(test_such.having a case inside the external fixture\)\n"
            "StopLayerSetupTest: <class 'test_such.having a case inside the external fixture:layer'>:test 0000: should still have access to that fixture \(test_such.having a case inside the external fixture\)\n"
            "StartLayerTeardownTest: <class 'test_such.having a case inside the external fixture:layer'>:test 0000: should still have access to that fixture \(test_such.having a case inside the external fixture\)\n"
            "StopLayerTeardownTest: <class 'test_such.having a case inside the external fixture:layer'>:test 0000: should still have access to that fixture \(test_such.having a case inside the external fixture\)\n"
            "StartLayerTeardown: <class 'test_such.having a case inside the external fixture:layer'>\n"
            "StopLayerTeardown: <class 'test_such.having a case inside the external fixture:layer'>\n"
            "StartLayerTeardown: <class 'test_such.having a different precondition:layer'>\n"
            "StopLayerTeardown: <class 'test_such.having a different precondition:layer'>\n"
            "StartLayerTeardown: <class 'test_such.SomeLayer'>\n"
            "StopLayerTeardown: <class 'test_such.SomeLayer'>\n"
            "StartLayerTeardown: <class 'test_such.having an expensive fixture:layer'>\n"
            "StopLayerTeardown: <class 'test_such.having an expensive fixture:layer'>\n"
            "StartLayerTeardown: <class 'test_such.A system with complex setup:layer'>\n"
            "StopLayerTeardown: <class 'test_such.A system with complex setup:layer'>\n*"
            "$"
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 9 tests')
        self.assertTestRunOutputMatches(proc, stdout=expected)
        self.assertEqual(proc.poll(), 0, proc.stderr.getvalue())

    def test_simple_layers(self):
        proc = self.runIn(
            'scenario/layers_hooks',
            '--plugin=nose2.plugins.layers',
            '--plugin=layer_hooks_plugin',
            'test_layers_simple')
        expected = (
            "^"
            "StartLayerSetup: <class 'test_layers_simple.Layer1'>\n"
            "StopLayerSetup: <class 'test_layers_simple.Layer1'>\n"
            "StartLayerSetupTest: <class 'test_layers_simple.Layer1'>:test_1 \(test_layers_simple.TestSimple\)\n"
            "StopLayerSetupTest: <class 'test_layers_simple.Layer1'>:test_1 \(test_layers_simple.TestSimple\)\n"
            "StartLayerTeardownTest: <class 'test_layers_simple.Layer1'>:test_1 \(test_layers_simple.TestSimple\)\n"
            "StopLayerTeardownTest: <class 'test_layers_simple.Layer1'>:test_1 \(test_layers_simple.TestSimple\)\n"
            "StartLayerSetupTest: <class 'test_layers_simple.Layer1'>:test_2 \(test_layers_simple.TestSimple\)\n"
            "StopLayerSetupTest: <class 'test_layers_simple.Layer1'>:test_2 \(test_layers_simple.TestSimple\)\n"
            "StartLayerTeardownTest: <class 'test_layers_simple.Layer1'>:test_2 \(test_layers_simple.TestSimple\)\n"
            "StopLayerTeardownTest: <class 'test_layers_simple.Layer1'>:test_2 \(test_layers_simple.TestSimple\)\n"
            "StartLayerTeardown: <class 'test_layers_simple.Layer1'>\n"
            "StopLayerTeardown: <class 'test_layers_simple.Layer1'>\n*"
            "$")
        self.assertTestRunOutputMatches(proc, stderr='Ran 2 tests')
        self.assertTestRunOutputMatches(proc, stdout=expected)
        self.assertEqual(proc.poll(), 0, proc.stderr.getvalue())
