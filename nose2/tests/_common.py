"""Common functionality."""
import os.path
import tempfile
import shutil
import sys
import subprocess
import unittest2

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, '..', '..')
SUPPORT = os.path.join(ROOT, 'support')


class TestCase(unittest2.TestCase):
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


class FunctionalTestCase(unittest2.TestCase):

    tags = ['functional']

    def assertTestRunOutputMatches(self, proc, stdout=None, stderr=None):
        cmd_stdout, cmd_stderr = proc.communicate()
        if stdout:
            self.assertRegexpMatches(cmd_stdout, stdout)
        if stderr:
            self.assertRegexpMatches(cmd_stderr, stderr)

    def runIn(self, testdir, *args):
        cmd = ['nose2'] + list(args)
        proc = subprocess.Popen(cmd, 
                                cwd=os.path.join(SUPPORT, testdir),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        return proc


class _FakeEventBase(object):
    """Baseclass for fake Events."""
