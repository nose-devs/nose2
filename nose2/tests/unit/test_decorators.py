"""
Unit tests for nose2 decorators.
"""

from nose2.tests._common import TestCase
from nose2.tools.decorators import with_setup, with_teardown


class WithSetupDecoratorTests(TestCase):
    def fake_setup(self):
        pass

    class fake_test:
        setup = None

    def test_setup_injection(self):
        sut = self.fake_test()
        expected = with_setup(self.fake_setup)(sut).setup

        self.assertEqual(expected, self.fake_setup)


class WithTeardownDecoratorTests(TestCase):
    def fake_teardown(self):
        pass

    class fake_test:
        teardown = None

    def test_teardown_injection(self):
        sut = self.fake_test()
        expected = with_teardown(self.fake_teardown)(sut).tearDownFunc

        self.assertEqual(expected, self.fake_teardown)
