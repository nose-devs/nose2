import logging
import sys
import unittest

from nose2 import events, util

log = logging.getLogger(__name__)

__unittest = True

#
# Layer suite class
#


class LayerSuite(unittest.BaseTestSuite):
    def __init__(self, session, tests=(), layer=None):
        super().__init__(tests)
        self.layer = layer
        self.wasSetup = False
        self.session = session

    def run(self, result):
        self.handle_previous_test_teardown(result)
        if not self._safeMethodCall(self.setUp, result):
            return
        try:
            for test in self:
                if result.shouldStop:
                    break
                self._safeMethodCall(self.setUpTest, result, test)
                try:
                    test(result)
                finally:
                    self._safeMethodCall(self.tearDownTest, result, test)
        finally:
            if self.wasSetup:
                self._safeMethodCall(self.tearDown, result)

    def handle_previous_test_teardown(self, result):
        prev = getattr(result, "_previousTestClass", None)
        if prev is None:
            return
        layer_attr = getattr(prev, "layer", None)
        if isinstance(layer_attr, LayerSuite):
            return
        try:
            suite_obj = unittest.suite.TestSuite()
            suite_obj._tearDownPreviousClass(None, result)
            suite_obj._handleModuleTearDown(result)
        finally:
            result._previousTestClass = None

    def setUp(self):
        if self.layer is None:
            return

        event = events.StartLayerSetupEvent(self.layer)
        self.session.hooks.startLayerSetup(event)

        setup = self._getBoundClassmethod(self.layer, "setUp")

        if setup:
            setup()
        self.wasSetup = True

        event = events.StopLayerSetupEvent(self.layer)
        self.session.hooks.stopLayerSetup(event)

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
        if getattr(test, "_layer_wasSetUp", False):
            return

        event = events.StartLayerSetupTestEvent(self.layer, test)
        self.session.hooks.startLayerSetupTest(event)

        self._allLayers(test, "testSetUp")
        test._layer_wasSetUp = True

        event = events.StopLayerSetupTestEvent(self.layer, test)
        self.session.hooks.stopLayerSetupTest(event)

    def tearDownTest(self, test):
        if self.layer is None:
            return
        if not getattr(test, "_layer_wasSetUp", None):
            return

        event = events.StartLayerTeardownTestEvent(self.layer, test)
        self.session.hooks.startLayerTeardownTest(event)

        self._allLayers(test, "testTearDown", reverse=True)

        event = events.StopLayerTeardownTestEvent(self.layer, test)
        self.session.hooks.stopLayerTeardownTest(event)
        delattr(test, "_layer_wasSetUp")

    def tearDown(self):
        if self.layer is None:
            return

        event = events.StartLayerTeardownEvent(self.layer)
        self.session.hooks.startLayerTeardown(event)
        teardown = self._getBoundClassmethod(self.layer, "tearDown")
        if teardown:
            teardown()
        event = events.StopLayerTeardownEvent(self.layer)
        self.session.hooks.stopLayerTeardown(event)

    def _safeMethodCall(self, method, result, *args):
        try:
            method(*args)
            return True
        except KeyboardInterrupt:
            raise
        except BaseException:
            result.addError(self, sys.exc_info())
            return False

    def _allLayers(self, test, method, reverse=False):
        done = set()
        all_lys = util.ancestry(self.layer)
        if reverse:
            all_lys = [reversed(lys) for lys in reversed(all_lys)]
        for lys in all_lys:
            for layer in lys:
                if layer in done:
                    continue
                self._inLayer(layer, test, method)
                done.add(layer)

    def _inLayer(self, layer, test, method):
        meth = self._getBoundClassmethod(layer, method)
        if meth:
            if util.num_expected_args(meth) > 1:
                meth(test)
            else:
                meth()

    def _getBoundClassmethod(self, cls, method):
        """
        Use instead of :func:`getattr` to get only classmethods explicitly
        defined on ``cls`` (not methods inherited from ancestors)
        """
        descriptor = cls.__dict__.get(method, None)
        if descriptor:
            if not isinstance(descriptor, classmethod):
                raise TypeError(
                    "The %s method on a layer must be a classmethod." % method
                )
            bound_method = descriptor.__get__(None, cls)
            return bound_method
        else:
            return None
