import os.path
import shutil
import tempfile
import unittest


class Test(unittest.TestCase):

    def setUp(self):
        super(Test, self).setUp()

        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        super(Test, self).tearDown()

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_chdir(self):
        os.chdir(self.temp_dir)
