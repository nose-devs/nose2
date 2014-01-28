import unittest

from nose2 import session
from nose2.plugins import dundertest
from nose2.tests._common import TestCase


class TestDunderTestPlugin(TestCase):
    tags = ['unit']

    def setUp(self):
        self.suite = unittest.TestSuite()
        self.caseClass = TestCase
        self.session = session.Session()
        self.plugin = dundertest.DunderTestFilter(session=self.session)
        self.plugin.register()

    def test_undefined_dunder_test_attribute_keeps_test(self):
        self.suite.addTest(self.caseClass())
        self.plugin.removeNonTests(self.suite)
        self.assertEquals(len(list(self.suite)), 1)

    def test_false_dunder_test_attribute_removes_test(self):
        dummyTest = self.caseClass()
        dummyTest.__test__ = False
        self.suite.addTest(dummyTest)
        self.plugin.removeNonTests(self.suite)
        self.assertEquals(len(list(self.suite)), 0)
