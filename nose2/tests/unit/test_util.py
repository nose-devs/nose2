import os
import sys

from nose2.tests._common import TestCase
from nose2 import util


class UtilTests(TestCase):
    _RUN_IN_TEMP = True

    def test_ensure_importable(self):
        test_dir = os.path.join(self._work_dir, 'test_dir')
        # Make sure test data is suitable for the test
        self.assertNotIn(test_dir, sys.path)
        util.ensure_importable(test_dir)
        self.assertEqual(test_dir, sys.path[0])
