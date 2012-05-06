from nose2.compat import unittest
from nose2.plugins import layers
from nose2 import events, loader, session
from nose2.tests._common import TestCase


class TestLayers(TestCase):
    tags = ['unit']

    def setUp(self):
        self.session = session.Session()
        self.loader = loader.PluggableTestLoader(session=self.session)
        self.session.testLoader = self.loader
        self.plugin = layers.Layers(session=self.session)

    def test_simple_layer_inheritance(self):
        class L1(object):
            pass
        class L2(L1):
            pass
        class T1(unittest.TestCase):
            layer = L1
            def test(self):
                pass
        class T2(unittest.TestCase):
            layer = L2
            def test(self):
                pass

        suite = unittest.TestSuite([T2('test'), T1('test')])
        event = events.StartTestRunEvent(None, suite, None, 0, None)
        self.plugin.startTestRun(event)
        expect = [['test (nose2.tests.unit.test_layers_plugin.T1)',
                   ['test (nose2.tests.unit.test_layers_plugin.T2)']]]
        self.assertEqual(self.names(event.suite), expect)

    def names(self, suite):
        n = []
        for t in suite:
            if isinstance(t, unittest.TestCase):
                n.append(str(t))
            else:
                n.append(self.names(t))
        return n
