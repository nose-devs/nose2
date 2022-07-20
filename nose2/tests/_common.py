"""Common functionality."""
import io
import os.path
import platform
import shutil
import subprocess
import sys
import tempfile
import unittest

from nose2 import discover, util

HERE = os.path.abspath(os.path.dirname(__file__))
SUPPORT = os.path.join(HERE, "functional", "support")


class TestCase(unittest.TestCase):

    """TestCase extension.

    If the class variable ``_RUN_IN_TEMP`` is ``True`` (default: ``False``), tests will
    be performed in a temporary directory, which is deleted afterwards.
    """

    _RUN_IN_TEMP = False

    def setUp(self):
        super().setUp()

        if self._RUN_IN_TEMP:
            self._orig_dir = os.getcwd()
            work_dir = self._work_dir = tempfile.mkdtemp()
            os.chdir(self._work_dir)
            # Make sure it's possible to import modules from current directory
            sys.path.insert(0, work_dir)

    def tearDown(self):
        super().tearDown()

        if self._RUN_IN_TEMP:
            os.chdir(self._orig_dir)
            shutil.rmtree(self._work_dir, ignore_errors=True)

    def __str__(self):
        """
        In python 3.5, the unittest.TestCase.__str__() output changed.
        This makes it conform to previous version.
        """
        test_module = self.__class__.__module__
        test_class = self.__class__.__name__
        test_method = self._testMethodName
        return f"{test_method} ({test_module}.{test_class})"

    def id(self):
        """
        In python 3.5, the unittest.TestCase.__id__() output changed.
        This makes it conform to previous version.
        """
        test_module = self.__class__.__module__
        test_class = self.__class__.__name__
        test_method = self._testMethodName
        return f"{test_module}.{test_class}.{test_method}"


class FunctionalTestCase(unittest.TestCase):
    tags = ["functional"]

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
            self.assertRegex(util.safe_decode(cmd_stdout), stdout)
        if stderr:
            self.assertRegex(util.safe_decode(cmd_stderr), stderr)

    def runIn(self, testdir, *args, **kw):
        return run_nose2(*args, cwd=testdir, **kw)

    def runModuleAsMain(self, testmodule, *args):
        return run_module_as_main(testmodule, *args)


class _FakeEventBase:

    """Baseclass for fake :class:`~nose2.events.Event`s."""

    def __init__(self):
        self.handled = False
        self.version = "0.1"
        self.metadata = {}


class FakeHandleFileEvent(_FakeEventBase):

    """Fake HandleFileEvent."""

    def __init__(self, name):
        super().__init__()

        self.loader = Stub()  # FIXME
        self.name = name
        self.path = os.path.split(name)[1]
        self.extraTests = []


class FakeStartTestEvent(_FakeEventBase):

    """Fake :class:`~nose2.events.StartTestEvent`."""

    def __init__(self, test):
        super().__init__()
        self.test = test
        self.result = test.defaultTestResult()
        import time

        self.startTime = time.time()


class FakeLoadFromNameEvent(_FakeEventBase):

    """Fake :class:`~nose2.events.LoadFromNameEvent`."""

    def __init__(self, name):
        super().__init__()
        self.name = name


class FakeLoadFromNamesEvent(_FakeEventBase):

    """Fake :class:`~nose2.events.LoadFromNamesEvent`."""

    def __init__(self, names):
        super().__init__()
        self.names = names


class FakeStartTestRunEvent(_FakeEventBase):

    """Fake :class:`~nose2.events.StartTestRunEvent`"""

    def __init__(
        self, runner=None, suite=None, result=None, startTime=None, executeTests=None
    ):
        super().__init__()
        self.suite = suite
        self.runner = runner
        self.result = result
        self.startTime = startTime
        self.executeTests = executeTests


class Stub:

    """Stub object for use in tests"""

    def __getattr__(self, attr):
        return Stub()

    def __call__(self, *arg, **kw):
        return Stub()


def support_file(*path_parts):
    return os.path.abspath(os.path.join(SUPPORT, *path_parts))


def run_nose2(*nose2_args, **nose2_kwargs):
    if "cwd" in nose2_kwargs:
        cwd = nose2_kwargs.pop("cwd")
        if not os.path.isabs(cwd):
            nose2_kwargs["cwd"] = support_file(cwd)
    return NotReallyAProc(nose2_args, **nose2_kwargs)


def run_module_as_main(test_module, *args):
    if not os.path.isabs(test_module):
        test_module = support_file(test_module)
    return subprocess.Popen(
        [sys.executable, test_module] + list(args),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


class NotReallyAProc:
    def __init__(self, args, cwd=None, **kwargs):
        self.args = args
        self.chdir = cwd
        self.kwargs = kwargs
        self.result = None
        self._exit_code = None

    def __enter__(self):
        self._stdout = sys.__stdout__
        self._stderr = sys.__stderr__
        self.cwd = os.getcwd()
        if self.chdir:
            os.chdir(self.chdir)
        self.stdout = sys.stdout = sys.__stdout__ = io.StringIO()
        self.stderr = sys.stderr = sys.__stderr__ = io.StringIO()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = sys.__stdout__ = self._stdout
        sys.stderr = sys.__stderr__ = self._stderr
        if self.chdir:
            os.chdir(self.cwd)
        return False

    def communicate(self):
        with self:
            try:
                self.result = discover(
                    argv=("nose2",) + self.args, exit=False, **self.kwargs
                )
            except SystemExit as e:
                self._exit_code = e.code
            return self.stdout.getvalue(), self.stderr.getvalue()

    @property
    def pid(self):
        return id(self)

    def poll(self):
        if self.result is None:
            return self._exit_code if self._exit_code is not None else 1

        # subprocess.poll should return None or the Integer exitcode
        return int(not self.result.result.wasSuccessful())


class RedirectStdStreams:

    """
    Context manager that replaces the stdin/stdout streams with :class:`StringIO`
    buffers.
    """

    def __init__(self):
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush()
        self.old_stderr.flush()
        sys.stdout, sys.stderr = self.stdout, self.stderr
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stdout.flush()
        self.stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr


# mock multiprocessing Connection
class Conn:
    def __init__(self, items):
        self.items = items
        self.sent = []
        self.closed = False

    def recv(self):
        if self.closed:
            raise EOFError("closed")
        try:
            return self.items.pop(0)
        except Exception:
            raise EOFError("EOF")

    def send(self, item):
        self.sent.append(item)

    def close(self):
        self.closed = True


# true on GitHub Actions, false otherwise
def environment_is_ci():
    return os.getenv("CI") == "true"


# special skip decorator for tests which are broken in Windows in CI
def windows_ci_skip(f):
    return unittest.skipIf(
        platform.system() == "Windows" and environment_is_ci(),
        "This test is skipped on Windows in CI",
    )(f)


def _method_name(name="test"):
    """Get an extra method name for Python 3.11"""
    # https://github.com/python/cpython/issues/58473
    return r"\." + name if sys.version_info >= (3, 11) else ""
