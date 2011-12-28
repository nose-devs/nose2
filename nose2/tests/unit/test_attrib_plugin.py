from nose2.plugins import attrib
from nose2.tests._common import TestCase


class TestAttribPlugin(TestCase):
    tags = ['unit']

    def setUp(self):
        class TC_1(TestCase):
            tags = ['a', 'b']
            def test_a(self):
                pass
            test_a.a = 1
            test_a.c = 0

            def test_b(self):
                pass
            test_b.b = 1
        self.TC_1 = TC_1
        self.plugin = attrib.AttributeSelector()

    def test_validate_attribs_with_simple_values(self):
        assert self.plugin.validateAttrib(
            self.TC_1('test_a'), [[('a', '1')]])
        assert self.plugin.validateAttrib(
            self.TC_1('test_a'), [[('a', True)]])
        assert self.plugin.validateAttrib(
            self.TC_1('test_a'), [[('c', False)]])
        assert self.plugin.validateAttrib(
            self.TC_1('test_b'), [[('b', '1')]])
        assert not self.plugin.validateAttrib(
            self.TC_1('test_a'), [[('a', False)]])
        assert not self.plugin.validateAttrib(
            self.TC_1('test_a'), [[('c', True)]])
        assert not self.plugin.validateAttrib(
            self.TC_1('test_a'), [[('a', '2')]])
        assert not self.plugin.validateAttrib(
            self.TC_1('test_a'), [[('b', '1')]])

    def test_validate_attribs_with_callable(self):
        assert self.plugin.validateAttrib(
            self.TC_1('test_a'), [[('a', lambda key, test: True)]])
        assert not self.plugin.validateAttrib(
            self.TC_1('test_a'), [[('a', lambda key, test: False)]])

    def test_validate_attribs_against_list(self):
        assert self.plugin.validateAttrib(
            self.TC_1('test_a'), [[('tags', 'a')]])
        assert self.plugin.validateAttrib(
            self.TC_1('test_a'), [[('tags', 'b')]])
        assert not self.plugin.validateAttrib(
            self.TC_1('test_a'), [[('tags', 'c')]])

