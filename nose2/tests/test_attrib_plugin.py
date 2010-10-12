import unittest2

from ..plugins import attrib


class TestAttribPlugin(unittest2.TestCase):
    tags = ['unit']

    def setUp(self):
        class TC_1(unittest2.TestCase):
            tags = ['a, b']
            def test_a(self):
                pass
            test_a.a = 1

            def test_b(self):
                pass
            test_b.b = 1
        self.TC_1 = TC_1
        self.plugin = attrib.AttributeSelector()

    def test_validate_attribs(self):
        assert self.plugin.validateAttrib(
            self.TC_1('test_a'), [[('a', '1')]])
        assert not self.plugin.validateAttrib(
            self.TC_1('test_a'), [[('b', '1')]])

