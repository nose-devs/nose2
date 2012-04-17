from contextlib import contextmanager
import inspect

from nose2.compat import unittest


__unittest = True


@contextmanager
def A(description):
    """Test scenario context manager.

    Returns a :class:`nose2.tools.such.Scenario` instance,
    which by convention is bound to ``it``:

    .. code-block :: python

      with such.A('test scenario') as it:
          # tests and fixtures

    """
    yield Scenario(description)


class Helper(unittest.TestCase):
    def runTest(self):
        pass


helper = Helper()


class Scenario(object):
    """A test scenario.

    A test scenario defines a set of fixtures and tests
    that depend on those fixtures.
    """
    _helper = helper

    def __init__(self, description):
        self._group = Group('A %s' % description, 0)

    @contextmanager
    def having(self, description):
        """Define a new fixture under the current fixture"""
        last = self._group
        self._group = self._group.child(
            "having %s" % description)
        yield self
        self._group = last

    def has_setup(self, func):
        self._group.addSetup(func)
        return func

    def has_teardown(self, func):
        self._group.addTeardown(func)
        return func

    def has_test_setup(self, func):
        self._group.addTestSetUp(func)

    def has_test_teardown(self, func):
        self._group.addTestTearDown(func)

    def should(self, desc):
        def decorator(f):
            _desc = desc if isinstance(desc, basestring) else f.__doc__
            case = Case(self._group, f, "should %s" % _desc)
            self._group.addCase(case)
            return case
        if type(desc) == type(decorator):
            return decorator(desc)
        return decorator

    def __getattr__(self, attr):
        return getattr(self._helper, attr)

    def createTests(self, mod):
        self._makeGroupTest(mod, self._group)

    def _makeGroupTest(self, mod, group, parent_layer=None):
        layer = self._makeLayer(group, parent_layer)
        case = self._makeTestCase(group, layer)
        mod[layer.__name__] =  layer
        layer.__module__ = mod['__name__']
        mod[case.__name__] =  case
        case.__module__ = mod['__name__']
        for child in group._children:
            self._makeGroupTest(mod, child, layer)

    def _makeTestCase(self, group, layer):
        attr = {
            'layer': layer,
            'group': group,
            'description': group.description,
            }

        for case in group._cases:
            def _test(s, case=case):
                case(s)
            name = 'test: %s' % case.description
            _test.__name__ = name
            _test.description = case.description
            _test.case = case
            attr[name] = _test

        setups = group._test_setups[:]
        teardowns = group._test_teardowns[:]
        if setups:
            def setUp(self):
                for func in setups:
                    args, _, _, _ = inspect.getargspec(func)
                    if args:
                        func(self)
                    else:
                        func()
            attr['setUp'] = setUp
        if teardowns:
            def tearDown(self):
                for func in teardowns:
                    args, _, _, _ = inspect.getargspec(func)
                    if args:
                        func(self)
                    else:
                        func()
            attr['tearDown'] = tearDown

        def methodDescription(self):
            return getattr(self, self._testMethodName).description
        attr['methodDescription'] = methodDescription

        return type(group.description, (unittest.TestCase,), attr)

    def _makeLayer(self, group, parent_layer=None):
        if parent_layer is None:
            parent_layer = object

        # FIXME test setups
        #test_setups = group._test_setups[:]
        #test_teardowns = group._testeardowns[:]

        def setUp(cls):
            for setup in cls.setups:
                setup()

        def tearDown(cls):
            for teardown in cls.teardowns:
                teardown()

        attr = {
            'description': group.description,
            'setUp': classmethod(setUp),
            'tearDown': classmethod(tearDown),
            'setups': group._setups[:],
            'teardowns': group._teardowns[:],
            }

        return type("%s:layer" % group.description, (parent_layer, ), attr)



class Group(object):
    """Group of tests w/common fixtures & description"""
    def __init__(self, description, indent=0, parent=None):
        self.description = description
        self.indent = indent
        self.parent = parent
        self._cases = []
        self._setups = []
        self._teardowns = []
        self._test_setups = []
        self._test_teardowns = []
        self._children = []

    def addCase(self, case):
        if not self._cases:
            case.first = True
        case.indent = self.indent
        self._cases.append(case)

    def addSetup(self, func):
        self._setups.append(func)

    def addTeardown(self, func):
        self._teardowns.append(func)

    def addTestSetUp(self, func):
        self._test_setups.append(func)

    def addTestTearDown(self, func):
        self._test_teardowns.append(func)

    def fullDescription(self):
        d = []
        p = self.parent
        while p:
            d.insert(0, p.description)
            p = p.parent
        d.append(self.description)
        return ' '.join(d)

    def child(self, description):
        child = Group(description, self.indent+1, self)
        self._children.append(child)
        return child


class Case(object):
    """Information about a test case"""
    _helper = helper

    def __init__(self, group, func, description):
        self.group = group
        self.func = func
        self.description = description
        self._setups = []
        self._teardowns = []
        self.first = False
        self.full = False

    def __call__(self, testcase):
        # ... only if it takes an arg
        self._helper = testcase
        args, _, _, _ = inspect.getargspec(self.func)
        if args:
            self.func(testcase)
        else:
            self.func()

    def __getattr__(self, attr):
        return getattr(self._helper, attr)
