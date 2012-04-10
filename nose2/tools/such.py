from contextlib import contextmanager
import inspect
import re
import unittest



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
        self._group = Group(self.format('*A* ') + description, 0)

    @contextmanager
    def having(self, description):
        last = self._group
        self._group = self._group.child(
            self.format("*... with* ") + description)
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

    # has_setup_each or similar name for per-test fixture

    def should(self, desc):
        def decorator(f):
            _desc = desc if isinstance(desc, basestring) else f.__desc__
            case = Case(self._group, f, self.format("*should* ") + _desc)
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

    @property
    def TestCase(self):
        """Make test case (class) that runs all of my tests"""
        return self._group.TestCase


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

    @property
    def TestCase(self):
        # FIXME this has to return a test case CLASS not instance
        desc = "%s%s" % ('  ' * self.indent, self.description)
        return make_test_case(
            desc, self._cases, self._setups, self._teardowns, self._children)


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

    # makes no sense here move up
    def has_setup(self, func):
        self._setups.append(func)

    def has_teardown(self, func):
        self._teardowns.append(func)

    def __call__(self):
        # ... only if it takes an arg
        args, _, _, _ = inspect.getargspec(self.func)
        if args:
            self.func(self)
        else:
            self.func()

    def __getattr__(self, attr):
        return getattr(self._helper, attr)

    @property
    def Test(self):
        return ShouldTestCase(self, setUp=self._setups, tearDown=self._teardowns,
                              description=self.description, first=self.first)


def make_test_case(desc, cases, setups, teardowns, children):
    class GroupTestCase(unittest.TestCase):
        _description = desc
        _setups = setups
        # unittest2 already has a _teardowns attribute
        _cleans = teardowns
        _cases = cases
        _children = children

        # FIXME

        # some way to set attributes on this class
        # or use getattr to make it possible to
        # load individual cases by name?

        def __init__(self, *arg, **kw):
            self.suite = unittest.TestSuite()
            self._teardown_in_teardown = not hasattr(self, 'addTeardown')
            for case in self._cases:
                self.suite.addTest(case.Test)
            for child in self._children:
                self.suite.addTest(child.TestCase())
            if not self._teardown_in_teardown:
                for teardown in teardowns:
                    self.addCleanup(teardown)

            self._testMethodName = None

        def setUp(self):
            for setup in self._setups:
                setup()

        def tearDown(self):
            if self._teardown_in_teardown:
                for func in self._cleans:
                    func()

        def run(self, result):
            # fixme do something better here
            result.startTest(self)
            self.setUp()
            try:
                self.suite(result)
            finally:
                self.tearDown()
                result.stopTest(self)

        def runTest(self):
            pass # trick unittest into running me

        def id(self):
            return self._description

        def shortDescription(self):
            return ''

        def __repr__(self):
            return '<TestGroup: %s>' % self._description

        def __str__(self):
            return self._description

    return GroupTestCase


class ShouldTestCase(unittest.TestCase):
    def __init__(self, testFunc, setUp=(), tearDown=(), description=None,
                 first=False):
        super(ShouldTestCase,self).__init__()
        self._setups = setUp
        self._teardowns = tearDown
        self._testFunc = testFunc
        self._description = description
        self.first = first
        self._27 = hasattr(self, 'addCleanup') # XXX add tds as cleanups

    def setUp(self):
        for func in self._setups:
            func()

    def runTest(self):
        self._testFunc()

    def tearDown(self):
        for func in self._teardowns:
            func()

    # output trickery
    def __str__(self):
        if self.first:
            if self._27:
                return ""
            else:
                return "\n%s" % self._get_desc()
        return self._get_desc()

    def shortDescription(self):
        if not self._testFunc.full:
            self._testFunc.full = True
        else:
            # import pdb; pdb.set_trace()
            return "%s %s" % (self._testFunc.group.fullDescription(),
                               self._description)
        if self.first or not self._27:
            if not self._27 and self.first:
                return '\n%s' % self._get_desc()
            return self._get_desc()
        return ''

    def _get_desc(self):
        if self.first:
            self.first = False
        return "%s    - %s" % ('  ' * self._testFunc.indent, self._description)
