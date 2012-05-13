import re

from nose2 import events
from nose2.suite import LayerSuite


BRIGHT = r'\033[1m'
RESET = r'\033[0m'


class Layers(events.Plugin):
    alwaysOn = True

    def startTestRun(self, event):
        event.suite = self._makeLayerSuite(event)

    def _makeLayerSuite(self, event):
        return self._sortByLayers(
            event.suite, self.session.testLoader.suiteClass)

    def _sortByLayers(self, suite, suiteClass):
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


class LayerReporter(events.Plugin):
    commandLineSwitch = (
        None, 'layer-reporter', 'Add layer information to test reports')
    configSection = 'layer-reporter'

    def __init__(self):
        self.indent = self.config.as_str('indent', '  ')
        self.colors = self.config.as_bool('colors', False)
        self.highlight_words = self.config.as_list('highlight-words',
                                                   ['A', 'having', 'should'])
        self.highlight_re = re.compile(
            r'\b(%s)\b' % '|'.join(self.highlight_words))
        self.layersReported = set()

    def reportStartTest(self, event):
        if self.session.verbosity < 2:
            return
        test = event.testEvent.test
        layer = getattr(test, 'layer', None)
        if not layer:
            return
        for ix, lys in enumerate(self.ancestry(layer)):
            for layer in lys:
                if layer not in self.layersReported:
                    desc = self.describeLayer(layer)
                    event.stream.writeln('%s%s' % (self.indent * ix, desc))
                    self.layersReported.add(layer)
        event.stream.write(self.indent * (ix+1))

    def describeLayer(self, layer):
        return self.format(getattr(layer, 'description', layer.__name__))

    def format(self, st):
        if self.colors:
            return self.highlight_re.sub(r'%s\1%s' % (BRIGHT, RESET), st)
        return st

    def describeTest(self, event):
        if hasattr(event.test, 'methodDescription'):
            event.description = self.format(event.test.methodDescription())
        if event.errorList and hasattr(event.test, 'layer'):
            # walk back layers to build full description
            self.describeLayers(event)

    def describeLayers(self, event):
        desc = [event.description]
        base = event.test.layer
        for layer in base.__mro__:
            if layer is object:
                break
            desc.append(self.describeLayer(layer))
        desc.reverse()
        event.description = ' '.join(desc)

    def ancestry(self, layer):
        layers = [[layer]]
        bases = [base for base in layer.__bases__
                 if base is not object]
        while bases:
            layers.append(bases)
            seen = set()
            newbases = []
            for b in bases:
                for bb in b.__bases__:
                    if bb is not object and bb not in seen:
                        newbases.append(bb)
            bases = newbases
        layers.reverse()
        return layers

