"""Common functionality."""
import os.path
import tempfile
import shutil
import sys

class TestCase(unittest2.TestCase):
    """TestCase extension.
    
    If the class variable _RUN_IN_TEMP is True (default: False), tests will be
    performed in a temporary directory, which is deleted afterwards.
    """
    _RUN_IN_TEMP = False

    def setUp(self):
        super(TestCase, self).setUp()
        
        if self._RUN_IN_TEMP:
            self.__orig_dir = os.getcwd()
            work_dir = self.__work_dir = tempfile.mkdtemp()
            os.chdir(self.__work_dir)
            # Make sure it's possible to import modules from current directory
            sys.path.insert(0, work_dir)

    def tearDown(self):
        super(TestCase, self).tearDown()

        if self._RUN_IN_TEMP:
            os.chdir(self.__orig_dir)
            shutil.rmtree(self.__work_dir, ignore_errors=True)


class _FakeEventBase(object):
    """Baseclass for fake Events."""
