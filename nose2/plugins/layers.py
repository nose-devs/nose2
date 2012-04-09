import inspect

from nose2 import events
from nose2.compat import unittest


class Layers(events.Plugin):
    alwaysOn = True

    def startTestRun(self, event):
        event.suite = self._makeLayerSuite(event)

    def _makeLayerSuite(self, event):
        return self._sortByLayers(
            event.suite, self.session.testLoader.suiteClass)

    def _sortByLayers(self, suite, suiteClass):
        # top-level suite that we'll return
        top = suiteClass()
        # first find all of the layers mentioned
        layers = {}
        for test in self._flatten(suite):
            # split tests up into buckets by layer
            layer = getattr(test, 'layer', None)
            if layer:
                layers.setdefault(layer, LayerSuite(layer=layer)).addTest(test)
            else:
                top.addTest(test)

        # then organize layers into a tree
        remaining = list(layers.keys())
        seen = set()
        tree = {}
        while remaining:
            ly = remaining.pop()
            if ly in seen:
                continue
            seen.add(ly)
            # superclasses of this layer
            if ly is None:
                deps = []
            else:
                deps = [cls for cls in ly.__bases__
                        if cls is not object]
                deps.reverse()
            if not deps:
                # layer is top-level
                self._addToTree(tree, ly, None)
            else:
                #inner, outer = ly, deps.pop()
                #self._addToTree(tree, inner, outer)
                #if outer not in layers:
                #    remaining.append(outer)
                #    layers[outer] = LayerSuite(layer=outer)
                outer = ly
                while deps:
                    inner, outer = outer, deps.pop()
                    self._addToTree(tree, inner, outer)
                    if outer not in layers:
                        remaining.append(outer)
                        layers[outer] = LayerSuite(layer=outer)
                    seen.add(inner)


        # finally build the top-level suite
        self._treeToSuite(tree, None, top, layers)

        return top

    def _addToTree(self, tree, inner, outer):
        for k, v in tree.items():
            if inner in v:
                v.remove(inner)
                break
        tree.setdefault(outer, []).append(inner)

    def _treeToSuite(self, tree, key, suite, layers):
        mysuite = layers.get(key, None)
        if mysuite:
            suite.addTest(mysuite)
            suite = mysuite
        sublayers = tree.get(key, [])
        for layer in sublayers:
            self._treeToSuite(tree, layer, suite, layers)

    def _flatten(self, suite):
        out = []
        for test in suite:
            try:
                out.extend(self._flatten(test))
            except TypeError:
                out.append(test)
        return out


#
# Layer suite class
#
class LayerSuite(unittest.BaseTestSuite):
    def __init__(self, tests=(), layer=None):
        super(LayerSuite, self).__init__(tests)
        self.layer = layer
        self.wasSetup = False

    def run(self, result):
        self.setUp()
        try:
            for test in self:
                if result.shouldStop:
                    break
                self.setUpTest(test)
                try:
                    test(result)
                finally:
                    self.tearDownTest(test)
        finally:
            if self.wasSetup:
                self.tearDown()

    def setUp(self):
        if self.layer is None:
            return
        setup = getattr(self.layer, 'setUp', None)
        if setup:
            setup()
        self.wasSetup = True

    def setUpTest(self, test):
        if self.layer is None:
            return
        # skip suites, to ensure test setup only runs once around each test
        # even for sub-layer suites inside this suite.
        try:
            iter(test)
        except TypeError:
            # ok, not a suite
            pass
        else:
            # suite-like enough for skipping
            return

        setup = getattr(self.layer, 'testSetUp', None)
        if setup:
            if getattr(test, '_layer_wasSetUp', False):
                return
            args, _, _, _ = inspect.getargspec(setup)
            if len(args) > 1:
                setup(test)
            else:
                setup()
        test._layer_wasSetUp = True

    def tearDownTest(self, test):
        if self.layer is None:
            return
        if not getattr(test, '_layer_wasSetUp', None):
            return
        teardown = getattr(self.layer, 'testTearDown', None)
        if teardown:
            args, _, _, _ = inspect.getargspec(teardown)
            if len(args) > 1:
                teardown(test)
            else:
                teardown()
        delattr(test, '_layer_wasSetUp')

    def tearDown(self):
        if self.layer is None:
            return
        teardown = getattr(self.layer, 'tearDown', None)
        if teardown:
            teardown()
