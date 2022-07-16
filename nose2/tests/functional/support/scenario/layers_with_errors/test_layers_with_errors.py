import unittest


class Layer:
    description = "fixture with a value"

    @classmethod
    def setUp(cls):
        cls.value = 1


class Test(unittest.TestCase):
    layer = Layer

    def test_ok(self):
        self.assertEqual(self.layer.value, 1)

    def test_fail(self):
        self.assertEqual(self.layer.value, 2)

    def test_err(self):
        self.assertEqual(self.layer.mulch, "pine")
