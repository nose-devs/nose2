import os
import subprocess
import unittest2

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, '..', '..')
SUPPORT = os.path.join(ROOT, 'support')


class TestCase(unittest2.TestCase):

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
