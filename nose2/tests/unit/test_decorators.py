"""
Unit tests for nose2 decorators.
"""

from nose2.tests._common import TestCase
from nose2.tools.decorators import with_setup


class WithSetupDecoratorTests(TestCase):
    def fake_setup(self):
        pass

    class fake_test(object):
        setup = None

    def test_setup_injection(self):
        sut = self.fake_test()
        expected = with_setup(self.fake_setup)(sut).setup

        self.assertEquals(expected, self.fake_setup)
