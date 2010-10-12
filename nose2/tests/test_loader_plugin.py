import unittest2

from ..plugins import loader


class TestGeneratorUnpack(unittest2.TestCase):
    tags = ['unit']

    def setUp(self):
        self.expect = [(0, ('call', (0, 1))),
                       (1, ('call', (1, 2))),
                       (2, ('call', (2, 3))),]

    def test_unpack_handles_nose_style_generators(self):
        def gen():
            for i in range(0, 3):
                yield 'call', i, i + 1
        out = list(loader.Functions().unpack(gen()))
        self.assertEqual(out, self.expect)

    def test_unpack_handles_unittest2_style_generators(self):
        def gen():
            for i in range(0, 3):
                yield 'call', (i, i + 1)
        out = list(loader.Functions().unpack(gen()))
        self.assertEqual(out, self.expect)
