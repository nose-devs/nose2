"""Common functionality."""
import unittest2.loader
import os.path
import tempfile
import shutil

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
            self.__work_dir = tempfile.mkdtemp()
            os.chdir(self.__work_dir)

    def tearDown(self):
        super(TestCase, self).tearDown()

        if self._RUN_IN_TEMP:
            os.chdir(self.__orig_dir)
            shutil.rmtree(self.__work_dir, ignore_errors=True)


class _FakeEventBase(object):
    """Baseclass for fake Events."""

class FakeHandleFileEvent(_FakeEventBase):
    """Fake HandleFileEvent."""
    def __init__(self, name):
        super(FakeHandleFileEvent, self).__init__()

        self.loader = unittest2.loader.TestLoader()
        self.name = name
        self.path = os.path.split(name)[1]
        self.extraTests = []
