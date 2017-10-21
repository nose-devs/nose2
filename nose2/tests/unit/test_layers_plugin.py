import sys
import unittest
from nose2.plugins import layers
from nose2 import events, loader, session, exceptions
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

    def test_multiple_inheritance(self):
        class L1(object):
            pass

        class L2(L1):
            pass

        class L3(L1):
            pass

        class T1(unittest.TestCase):
            layer = L1

            def test(self):
                pass

        class T2(unittest.TestCase):
            layer = L2

            def test(self):
                pass

        class T3(unittest.TestCase):
            layer = L3

            def test(self):
                pass

        suite = unittest.TestSuite([T2('test'), T1('test'), T3('test')])
        event = events.StartTestRunEvent(None, suite, None, 0, None)
        self.plugin.startTestRun(event)
        expect = [['test (nose2.tests.unit.test_layers_plugin.T1)',
                   ['test (nose2.tests.unit.test_layers_plugin.T2)'],
                   ['test (nose2.tests.unit.test_layers_plugin.T3)']]]
        self.assertEqual(self.names(event.suite), expect)

    def test_deep_inheritance(self):
        class L1(object):
            pass

        class L2(L1):
            pass

        class L3(L1):
            pass

        class L4(L2, L1):
            pass

        class L5(L4):
            pass

        class T1(unittest.TestCase):
            layer = L1

            def test(self):
                pass

        class T2(unittest.TestCase):
            layer = L2

            def test(self):
                pass

        class T3(unittest.TestCase):
            layer = L3

            def test(self):
                pass

        class T4(unittest.TestCase):
            layer = L4

            def test(self):
                pass

        class T5(unittest.TestCase):
            layer = L5

            def test(self):
                pass

        suite = unittest.TestSuite([T2('test'), T1('test'), T3('test'),
                                    T4('test'), T5('test')])
        event = events.StartTestRunEvent(None, suite, None, 0, None)
        self.plugin.startTestRun(event)
        expect = [['test (nose2.tests.unit.test_layers_plugin.T1)',
                   ['test (nose2.tests.unit.test_layers_plugin.T2)',
                    ['test (nose2.tests.unit.test_layers_plugin.T4)',
                     ['test (nose2.tests.unit.test_layers_plugin.T5)']]],
                   ['test (nose2.tests.unit.test_layers_plugin.T3)']]]
        self.assertEqual(self.names(event.suite), expect)

    def test_mixed_layers_no_layers(self):
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

        class T3(unittest.TestCase):

            def test(self):
                pass

        suite = unittest.TestSuite([T2('test'), T1('test'), T3('test')])
        event = events.StartTestRunEvent(None, suite, None, 0, None)
        self.plugin.startTestRun(event)
        expect = ['test (nose2.tests.unit.test_layers_plugin.T3)',
                  ['test (nose2.tests.unit.test_layers_plugin.T1)',
                   ['test (nose2.tests.unit.test_layers_plugin.T2)']]]
        self.assertEqual(self.names(event.suite), expect)

    def test_ordered_layers(self):
        class L1(object):
            pass

        class L2(L1):
            position = 1

        class L3(L1):
            position = 2

        class L4(L1):
            position = 3

        class L5(L2):
            position = 4

        class T1(unittest.TestCase):
            layer = L1

            def test(self):
                pass

        class T2(unittest.TestCase):
            layer = L2

            def test(self):
                pass

        class T3(unittest.TestCase):
            layer = L3

            def test(self):
                pass

        class T4(unittest.TestCase):
            layer = L4

            def test(self):
                pass

        class T5(unittest.TestCase):
            layer = L5

            def test(self):
                pass
        suite = unittest.TestSuite([T2('test'), T1('test'),
                                    T3('test'), T4('test'), T5('test')])
        event = events.StartTestRunEvent(None, suite, None, 0, None)
        self.plugin.startTestRun(event)
        expect = [['test (nose2.tests.unit.test_layers_plugin.T1)',
                   ['test (nose2.tests.unit.test_layers_plugin.T2)',
                    ['test (nose2.tests.unit.test_layers_plugin.T5)', ]],
                   ['test (nose2.tests.unit.test_layers_plugin.T3)', ],
                   ['test (nose2.tests.unit.test_layers_plugin.T4)', ]]]
        self.assertEqual(self.names(event.suite), expect)

    def test_mixin_in_top_layer(self):

        class M1(object):
            pass

        class L1(object):
            mixins = (M1,)

        class T1(unittest.TestCase):
            layer = L1

            def test(self):
                pass

        suite = unittest.TestSuite([T1('test')])
        event = events.StartTestRunEvent(None, suite, None, 0, None)
        self.plugin.startTestRun(event)
        expect = [  # M1
                  [  # L1
                   [  # T1
                    'test (nose2.tests.unit.test_layers_plugin.T1)']]]
        self.assertEqual(self.names(event.suite), expect)

    def test_mixin_in_inner_layer(self):

        class M1(object):
            pass

        class L1(object):
            pass

        class L2(L1):
            mixins = (M1,)

        class T1(unittest.TestCase):
            layer = L1

            def test(self):
                pass

        class T2(unittest.TestCase):
            layer = L2

            def test(self):
                pass

        suite = unittest.TestSuite([T1('test'), T2('test')])
        event = events.StartTestRunEvent(None, suite, None, 0, None)
        self.plugin.startTestRun(event)
        expect = [  # L1
                  ['test (nose2.tests.unit.test_layers_plugin.T1)',
                   # M1
                   [  # L2
                    ['test (nose2.tests.unit.test_layers_plugin.T2)']]]]
        self.assertEqual(self.names(event.suite), expect)

    def test_mixin_inheritance(self):
        # without mixin
        # L1
        #  -> L3
        #   -> L4
        #    -> L5
        # L2
        #  -> L6
        #
        # with mixin new behavior:
        #   the mixin (L4, which comes with L3 and L1)
        #   is inserted after the parent layer (L2).
        # L2
        #  -> L1
        #   -> L3
        #    -> L4
        #     -> L6
        #     -> L5
        #
        # with mixin old behavior
        #   the mixin (L4, which comes with L3 and L1)
        #   is inserted before the parent layer (L2).
        # L1
        #  -> L3
        #   -> L4
        #    -> L2
        #     -> L6
        #    -> L5
        class L1(object):
            pass

        class L2(object):  # a mixin, doesn't share a base w/L1
            pass

        class L3(L1):
            pass

        class L4(L3):
            pass

        class L5(L4):
            pass

        class L6(L2):
            mixins = (L4,)

        class T1(unittest.TestCase):
            layer = L1

            def test(self):
                pass

        class T3(unittest.TestCase):
            layer = L3

            def test(self):
                pass

        class T4(unittest.TestCase):
            layer = L4

            def test(self):
                pass

        class T5(unittest.TestCase):
            layer = L5

            def test(self):
                pass

        class T6(unittest.TestCase):
            layer = L6

            def test(self):
                pass
        suite = unittest.TestSuite(
            [T6('test'), T1('test'), T3('test'), T4('test'), T5('test')])
        event = events.StartTestRunEvent(None, suite, None, 0, None)
        self.plugin.startTestRun(event)
        expect = [  # L2
                  [  # L1
                   ['test (nose2.tests.unit.test_layers_plugin.T1)',  # T1
                    # L3
                    ['test (nose2.tests.unit.test_layers_plugin.T3)',  # T3
                     # L4
                     ['test (nose2.tests.unit.test_layers_plugin.T4)',  # T4
                      # L5
                      ['test (nose2.tests.unit.test_layers_plugin.T5)'],
                      # L6
                      ['test (nose2.tests.unit.test_layers_plugin.T6)']]]]]]
        self.assertEqual(self.names(event.suite), expect)

    def test_invalid_top_layer(self):

        if sys.version_info >= (3, 0):
            # in python 3, L1 will automatically have `object` has base, so
            # this test does not make sense, and will actually fail.
            return

        class L1():
            pass

        class T1(unittest.TestCase):
            layer = L1

            def test(self):
                pass

        suite = unittest.TestSuite([T1('test')])
        event = events.StartTestRunEvent(None, suite, None, 0, None)
        with self.assertRaises(exceptions.LoadTestsFailure):
            self.plugin.startTestRun(event)

    def names(self, suite):
        return [n for n in self.iternames(suite)]

    def iternames(self, suite):
        for t in suite:
            if isinstance(t, unittest.TestCase):
                if sys.version_info >= (3, 5):
                    test_module = t.__class__.__module__
                    test_class = t.__class__.__name__
                    test_method = t._testMethodName
                    yield "%s (%s.%s)" % (test_method, test_module, test_class)
                else:
                    yield str(t)
            else:
                yield [n for n in self.iternames(t)]

    def _listset(self, l):
        n = set([])
        for t in l:
            if isinstance(t, list):
                n.add(self._listset(t))
            else:
                n.add(t)
        return frozenset(n)
