"""Common functionality."""
import os.path
import tempfile
import shutil
import sys
import subprocess

from nose2.compat import unittest
from nose2 import util


HERE = os.path.abspath(os.path.dirname(__file__))
SUPPORT = os.path.join(HERE, 'functional', 'support')


class TestCase(unittest.TestCase):
    """TestCase extension.

    If the class variable _RUN_IN_TEMP is True (default: False), tests will be
    performed in a temporary directory, which is deleted afterwards.
    """
    _RUN_IN_TEMP = False

    def setUp(self):
        super(TestCase, self).setUp()

        if self._RUN_IN_TEMP:
            self._orig_dir = os.getcwd()
            work_dir = self._work_dir = tempfile.mkdtemp()
            os.chdir(self._work_dir)
            # Make sure it's possible to import modules from current directory
            sys.path.insert(0, work_dir)

    def tearDown(self):
        super(TestCase, self).tearDown()

        if self._RUN_IN_TEMP:
            os.chdir(self._orig_dir)
            shutil.rmtree(self._work_dir, ignore_errors=True)


class FunctionalTestCase(unittest.TestCase):
    tags = ['functional']

    def assertTestRunOutputMatches(self, proc, stdout=None, stderr=None):
        cmd_stdout, cmd_stderr = None, None
        try:
            cmd_stdout, cmd_stderr = self._output[proc.pid]
        except AttributeError:
            self._output = {}
        except KeyError:
            pass
        if cmd_stdout is None:
            cmd_stdout, cmd_stderr = proc.communicate()
            self._output[proc.pid] = cmd_stdout, cmd_stderr
        if stdout:
            self.assertRegexpMatches(util.safe_decode(cmd_stdout), stdout)
        if stderr:
            self.assertRegexpMatches(util.safe_decode(cmd_stderr), stderr)

    def runIn(self, testdir, *args, **kw):
        return run_nose2(*args, cwd=testdir, **kw)


class _FakeEventBase(object):
    """Baseclass for fake Events."""
    def __init__(self):
        self.handled = False
        self.version = '0.1'
        self.metadata = {}


class FakeHandleFileEvent(_FakeEventBase):
    """Fake HandleFileEvent."""
    def __init__(self, name):
        super(FakeHandleFileEvent, self).__init__()

        self.loader = Stub() # FIXME
        self.name = name
        self.path = os.path.split(name)[1]
        self.extraTests = []


class FakeStartTestEvent(_FakeEventBase):
    """Fake StartTestEvent."""
    def __init__(self, test):
        super(FakeStartTestEvent, self).__init__()
        self.test = test
        self.result = test.defaultTestResult()
        import time
        self.startTime = time.time()


class FakeLoadFromNameEvent(_FakeEventBase):
    """Fake LoadFromNameEvent."""
    def __init__(self, name):
        super(FakeLoadFromNameEvent, self).__init__()
        self.name = name


class FakeLoadFromNamesEvent(_FakeEventBase):
    """Fake LoadFromNamesEvent."""
    def __init__(self, names):
        super(FakeLoadFromNamesEvent, self).__init__()
        self.names = names


class FakeStartTestRunEvent(_FakeEventBase):
    """Fake StartTestRunEvent"""
    def __init__(self, runner=None, suite=None, result=None, startTime=None,
                 executeTests=None):
        super(FakeStartTestRunEvent, self).__init__()
        self.suite = suite
        self.runner = runner
        self.result = result
        self.startTime = startTime
        self.executeTests = executeTests


class Stub(object):
    """Stub object for use in tests"""
    def __getattr__(self, attr):
        return Stub()
    def __call__(self, *arg, **kw):
        return Stub()


def support_file(*path_parts):
    return os.path.abspath(os.path.join(SUPPORT, *path_parts))


def run_nose2(*nose2_args, **popen_args):
    if 'cwd' in popen_args:
        cwd = popen_args.pop('cwd')
        if not os.path.isabs(cwd):
            popen_args['cwd'] = support_file(cwd)
    process = subprocess.Popen(
        ['python', '-m', 'nose2.__main__'] + list(nose2_args),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        **popen_args)
    return process
