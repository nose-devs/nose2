import logging
import re
from collections import OrderedDict

from nose2 import events, exceptions, util
from nose2.suite import LayerSuite

BRIGHT = r"\033[1m"
RESET = r"\033[0m"

__unittest = True

log = logging.getLogger(__name__)


class MissingParentLayer(Exception):
    pass


class Layers(events.Plugin):
    alwaysOn = True

    def startTestRun(self, event):
        event.suite = self.make_suite(event.suite, self.session.testLoader.suiteClass)

    def get_layers_from_suite(self, suite, suiteClass):
        top_layer = suiteClass()
        layers_dict = OrderedDict()
        for test in self.flatten_suite(suite):
            layer = getattr(test, "layer", None)
            if layer:
                if layer not in layers_dict:
                    layers_dict[layer] = LayerSuite(self.session, layer=layer)
                layers_dict[layer].addTest(test)
            else:
                top_layer.addTest(test)
        self.get_parent_layers(layers_dict)
        return top_layer, layers_dict

    def get_parent_layers(self, layers_dict):
        while True:
            missing_parents = []
            for layer in layers_dict.keys():
                for parent in layer.__bases__:
                    if parent is object:
                        continue
                    if parent not in layers_dict:
                        missing_parents.append(parent)
            if not missing_parents:
                break
            for parent in missing_parents:
                layers_dict[parent] = LayerSuite(self.session, layer=parent)

    def make_suite(self, suite, suiteClass):
        top_layer, layers_dict = self.get_layers_from_suite(suite, suiteClass)
        tree = {}
        unresolved_layers = self.update_layer_tree(tree, layers_dict.keys())
        while unresolved_layers:
            remaining = self.update_layer_tree(tree, unresolved_layers)
            if len(remaining) == len(unresolved_layers):
                raise exceptions.LoadTestsFailure(
                    "Could not resolve layer dependencies"
                )
            unresolved_layers = remaining
        for layer in tree.keys():
            if layer and layer not in layers_dict:
                layers_dict[layer] = LayerSuite(self.session, layer=layer)
        self.tree_to_suite(tree, None, top_layer, layers_dict)
        return top_layer

    @classmethod
    def update_layer_tree(cls, tree, layers):
        remaining = []
        for layer in layers:
            try:
                cls.add_layer_to_tree(tree, layer)
            except MissingParentLayer:
                remaining.append(layer)
        return remaining

    @classmethod
    def insert_mixins(cls, tree, layer, outer):
        mixins = getattr(layer, "mixins", None)
        if not mixins:
            return outer
        last = outer
        for mixin in mixins:
            mixin_ancestor = cls.get_oldest_parent(mixin)
            if last is None:
                tree.setdefault(None, []).append(mixin_ancestor)
            else:
                # The mixin_ancestor can be a layer that has been added to the
                # tree already. If so, it should a base layer, since it's the
                # last ancestor. We need to remove it from there, and insert it
                # in the "last" layer.
                if mixin_ancestor in tree[None]:
                    tree[None].remove(mixin_ancestor)
                tree[last].append(mixin_ancestor)
                if mixin_ancestor not in tree:
                    tree[mixin_ancestor] = []
            if mixin not in tree:
                tree[mixin] = []
            last = mixin
        return last

    @classmethod
    def insert_layer(cls, tree, layer, outer):
        if outer is object:
            outer = cls.insert_mixins(tree, layer, None)
        elif outer in tree:
            outer = cls.insert_mixins(tree, layer, outer)
        else:
            err = f"{outer} not found in {tree}"
            raise exceptions.LoadTestsFailure(err)
        if outer is None:
            tree.setdefault(None, []).append(layer)
        else:
            tree[outer].append(layer)
        tree[layer] = []

    @staticmethod
    def get_parents_from_tree(layer, tree):
        parents = []
        for key, value in tree.items():
            if layer in value:
                parents.append(key)

    @classmethod
    def get_oldest_parent(cls, layer):
        # FIXME: we assume that there is only one oldest parent
        # it should be the case most of the time but it will break sometimes.
        oldest = True
        for parent in layer.__bases__:
            if parent in [None, object]:
                continue
            else:
                oldest = False
                return cls.get_oldest_parent(parent)
        if oldest:
            return layer

    @classmethod
    def add_layer_to_tree(cls, tree, layer):
        parents = layer.__bases__
        if not parents:
            err = "Invalid layer {0}: should at least inherit from `object`"
            raise exceptions.LoadTestsFailure(err.format(layer))
        for parent in parents:
            if parent not in tree and parent is not object:
                raise MissingParentLayer
        # if we reached that point, then all the parents are in the tree
        # if there are multiple parents, we first try to get the closest
        # to the current layer.
        for parent in parents:
            if not cls.get_parents_from_tree(parent, tree):
                cls.insert_layer(tree, layer, parent)
                return
        raise exceptions.LoadTestsFailure(f"Failed to add {layer}")

    @classmethod
    def tree_to_suite(cls, tree, key, suite, layers):
        _suite = layers.get(key, None)
        if _suite:
            suite.addTest(_suite)
            suite = _suite
        sublayers = tree.get(key, [])
        # ensure that layers with a set order are in order
        sublayers.sort(key=cls.get_layer_position)
        for layer in sublayers:
            cls.tree_to_suite(tree, layer, suite, layers)

    @classmethod
    def flatten_suite(cls, suite):
        out = []
        for test in suite:
            try:
                out.extend(cls.flatten_suite(test))
            except TypeError:
                out.append(test)
        return out

    @staticmethod
    def get_layer_position(layer):
        pos = getattr(layer, "position", None)
        # ... lame
        if pos is not None:
            key = "%04d" % pos
        else:
            key = layer.__name__
        return key


class LayerReporter(events.Plugin):
    commandLineSwitch = (
        None,
        "layer-reporter",
        "Add layer information to test reports",
    )
    configSection = "layer-reporter"

    def __init__(self):
        self.indent = self.config.as_str("indent", "  ")
        self.colors = self.config.as_bool("colors", False)
        self.highlight_words = self.config.as_list(
            "highlight-words", ["A", "having", "should"]
        )
        self.highlight_re = re.compile(r"\b(%s)\b" % "|".join(self.highlight_words))
        self.layersReported = set()

    def reportStartTest(self, event):
        if self.session.verbosity < 2:
            return
        test = event.testEvent.test
        layer = getattr(test, "layer", None)
        if not layer:
            return
        for ix, lys in enumerate(util.ancestry(layer)):
            for layer in lys:
                if layer not in self.layersReported:
                    desc = self.describeLayer(layer)
                    event.stream.writeln(f"{self.indent * ix}{desc}")
                    self.layersReported.add(layer)
        event.stream.write(self.indent * (ix + 1))

    def describeLayer(self, layer):
        return self.format(getattr(layer, "description", layer.__name__))

    def format(self, st):
        if self.colors:
            return self.highlight_re.sub(rf"{BRIGHT}\1{RESET}", st)
        return st

    def describeTest(self, event):
        if hasattr(event.test, "methodDescription"):
            event.description = self.format(event.test.methodDescription())
        if event.errorList and hasattr(event.test, "layer"):
            # walk back layers to build full description
            self.describeLayers(event)
        # we need to remove "\n" from description to keep a well indented report when
        # tests have docstrings
        # see https://github.com/nose-devs/nose2/issues/327 for more information
        event.description = event.description.replace("\n", " ")

    def describeLayers(self, event):
        desc = [event.description]
        base = event.test.layer
        for layer in base.__mro__ + getattr(base, "mixins", ()):
            if layer is object:
                continue
            desc.append(self.describeLayer(layer))
        desc.reverse()
        event.description = " ".join(desc)


# for debugging
# def printtree(suite, indent=''):
#     import unittest
#     six.print_('%s%s ->' % (indent, getattr(suite, 'layer', 'no layer')))
#     for test in suite:
#         if isinstance(test, unittest.BaseTestSuite):
#             printtree(test, indent + '  ')
#         else:
#             six.print_('%s %s' % (indent, test))
#     six.print_('%s<- %s' % (indent, getattr(suite, 'layer', 'no layer')))
