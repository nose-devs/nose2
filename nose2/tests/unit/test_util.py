import os
import sys
import unittest

from nose2 import util
from nose2.tests._common import TestCase


class UtilTests(TestCase):
    _RUN_IN_TEMP = True

    def test_ensure_importable(self):
        test_dir = os.path.join(self._work_dir, "test_dir")
        # Make sure test data is suitable for the test
        self.assertNotIn(test_dir, sys.path)
        util.ensure_importable(test_dir)
        self.assertEqual(test_dir, sys.path[0])

    def test_testcase_test_name(self):
        test = UtilTests("test_ensure_importable")
        self.assertEqual(
            test.id(), "nose2.tests.unit.test_util.UtilTests.test_ensure_importable"
        )
        self.assertEqual(
            util.test_name(test),
            "nose2.tests.unit.test_util.UtilTests.test_ensure_importable",
        )

    def test_subtest_test_name(self):
        from unittest.case import _SubTest

        sentinel = getattr(unittest.case, "_subtest_msg_sentinel", None)
        test = UtilTests("test_ensure_importable")
        test = _SubTest(test, sentinel, {"i": 1, "j": 2})
        self.assertEqual(
            test.id(),
            "nose2.tests.unit.test_util.UtilTests.test_ensure_importable (i=1, j=2)",
        )
        self.assertEqual(
            util.test_name(test),
            "nose2.tests.unit.test_util.UtilTests.test_ensure_importable",
        )


class HasClassFixturesTests(TestCase):
    def test_unittest_testcase(self):
        C = unittest.TestCase
        self.assertFalse(util.has_class_fixtures(C))
        self.assertFalse(util.has_class_fixtures(C()))

    def test_derived_testcase(self):
        class C(unittest.TestCase):
            def runTest(self):
                pass

        self.assertFalse(util.has_class_fixtures(C))
        self.assertFalse(util.has_class_fixtures(C()))

    def test_testcase_with_setup(self):
        class C(unittest.TestCase):
            @classmethod
            def setUpClass(cls):
                pass

            def runTest(self):
                pass

        self.assertTrue(util.has_class_fixtures(C))
        self.assertTrue(util.has_class_fixtures(C()))

    def test_testcase_with_teardown(self):
        class C(unittest.TestCase):
            @classmethod
            def tearDownClass(cls):
                pass

            def runTest(self):
                pass

        self.assertTrue(util.has_class_fixtures(C))
        self.assertTrue(util.has_class_fixtures(C()))

    def test_derived_derived_testcase(self):
        class C(unittest.TestCase):
            @classmethod
            def setUpClass(cls):
                pass

            @classmethod
            def tearDownClass(cls):
                pass

        class D(C):
            def runTest(self):
                pass

        self.assertTrue(util.has_class_fixtures(D))
        self.assertTrue(util.has_class_fixtures(D()))


class HasModuleFixturesTests(TestCase):
    def test_module_without_fixtures(self):
        class M:
            pass

        M.__name__ = "nose2.foo.bar"

        class C(unittest.TestCase):
            def runTest(self):
                pass

        C.__module__ = M.__name__
        m = M()
        m.C = C
        sys.modules[M.__name__] = m
        try:
            self.assertFalse(util.has_module_fixtures(C))
            self.assertFalse(util.has_module_fixtures(C()))
        finally:
            del sys.modules[M.__name__]

    def test_module_with_setup(self):
        class M:
            pass

        M.__name__ = "nose2.foo.bar"

        class C(unittest.TestCase):
            def runTest(self):
                pass

        C.__module__ = M.__name__
        m = M()
        m.C = C
        m.setUpModule = lambda: None
        sys.modules[M.__name__] = m
        try:
            self.assertTrue(util.has_module_fixtures(C))
            self.assertTrue(util.has_module_fixtures(C()))
        finally:
            del sys.modules[M.__name__]

    def test_module_with_teardown(self):
        class M:
            pass

        M.__name__ = "nose2.foo.bar"

        class C(unittest.TestCase):
            def runTest(self):
                pass

        C.__module__ = M.__name__
        m = M()
        m.C = C
        m.tearDownModule = lambda: None
        sys.modules[M.__name__] = m
        try:
            self.assertTrue(util.has_module_fixtures(C))
            self.assertTrue(util.has_module_fixtures(C()))
        finally:
            del sys.modules[M.__name__]
