import os
import sys
import unittest

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

    def test_testcase_test_name(self):
        test = UtilTests('test_ensure_importable')
        self.assertEqual(test.id(),
            'nose2.tests.unit.test_util.UtilTests.test_ensure_importable')
        self.assertEqual(util.test_name(test),
            'nose2.tests.unit.test_util.UtilTests.test_ensure_importable')

    @unittest.skipIf(sys.version_info < (3, 4), 'Python >= 3.4 required')
    def test_subtest_test_name(self):
        from unittest.case import _SubTest
        sentinel = getattr(unittest.case, '_subtest_msg_sentinel', None)
        test = UtilTests('test_ensure_importable')
        test = _SubTest(test, sentinel, {'i': 1, 'j': 2})
        self.assertEqual(test.id(),
            'nose2.tests.unit.test_util.UtilTests.test_ensure_importable (i=1, j=2)')
        self.assertEqual(util.test_name(test),
            'nose2.tests.unit.test_util.UtilTests.test_ensure_importable')
