from nose2 import events
from nose2.suite import LayerSuite


class Layers(events.Plugin):
    alwaysOn = True

    def startTestRun(self, event):
        event.suite = self._makeLayerSuite(event)

    def _makeLayerSuite(self, event):
        return self._sortByLayers(
            event.suite, self.session.testLoader.suiteClass)

    def _sortByLayers(self, suite, suiteClass):
        # FIXME pass session to all suites
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


