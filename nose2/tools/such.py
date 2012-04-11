from contextlib import contextmanager
import inspect
import re

from nose2.compat import unittest


__unittest = True


@contextmanager
def A(description, colors=True):
    yield Scenario(description, colors)


class Helper(unittest.TestCase):
    def runTest(self):
        pass


helper = Helper()

BRIGHT = r'\033[1m'
RESET = r'\033[0m'


class Scenario(object):
    _helper = helper

    def __init__(self, description, colors=True):
        self.colors = colors
        self._group = Group('A %s' % description, 0)

    @contextmanager
    def having(self, description):
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
        pass # FIXME

    def has_test_teardown(self, func):
        pass # FIXME

    def should(self, desc):
        def decorator(f):
            _desc = desc if isinstance(desc, basestring) else f.__doc__
            case = Case(self._group, f, "should %s" % _desc)
            self._group.addCase(case)
            return case
        if type(desc) == type(decorator):
            return decorator(desc)
        return decorator

    def format(self, st):
        if self.colors:
            return re.sub(r'\*([^*]+)\*', r'%s\1%s' % (BRIGHT, RESET), st)
        return st

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
