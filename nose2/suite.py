import inspect
import logging

from nose2.compat import unittest

log = logging.getLogger(__name__)

__unittest = True

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
        # FIXME hook call
        log.debug('in setUp layer %s', self.layer)
        if self.layer is None:
            return

        setup = self._get_bound_classmethod(self.layer, 'setUp')
        if setup:
            setup()
            log.debug('setUp layer %s called', self.layer)
        self.wasSetup = True

    def setUpTest(self, test):
        # FIXME hook call
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

        setup = self._get_bound_classmethod(self.layer, 'testSetUp')
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
        # FIXME hook call
        if self.layer is None:
            return
        if not getattr(test, '_layer_wasSetUp', None):
            return
        teardown = self._get_bound_classmethod(self.layer, 'testTearDown')
        if teardown:
            args, _, _, _ = inspect.getargspec(teardown)
            if len(args) > 1:
                teardown(test)
            else:
                teardown()
        delattr(test, '_layer_wasSetUp')

    def tearDown(self):
        # FIXME hook call
        if self.layer is None:
            return

        teardown = self._get_bound_classmethod(self.layer, 'tearDown')
        if teardown:
            teardown()
            log.debug('tearDown layer %s called', self.layer)

    def _get_bound_classmethod(self, cls, method):
        """
        Use instead of getattr to get only classmethods explicitly defined
        on cls (not methods inherited from ancestors)
        """
        descriptor = cls.__dict__.get(method, None)
        if descriptor:
            if not isinstance(descriptor, classmethod):
                raise TypeError(
                    'The %s method on a layer must be a classmethod.' % method)
            bound_method = descriptor.__get__(None, cls)
            return bound_method
        else:
            return None

