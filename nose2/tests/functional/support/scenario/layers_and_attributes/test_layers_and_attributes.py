import unittest

STATE = {}


class L1:
    @classmethod
    def setUp(cls):
        STATE["L1"] = "setup"

    @classmethod
    def tearDown(cls):
        del STATE["L1"]


class L2:
    @classmethod
    def setUp(cls):
        STATE["L2"] = "setup"

    @classmethod
    def tearDown(cls):
        del STATE["L2"]


class LayerAndAttributesA(unittest.TestCase):
    layer = L1
    a = 1

    def test(self):
        self.assertEqual(STATE.get("L1"), "setup")


class LayerAndAttributesB(unittest.TestCase):
    layer = L2
    b = 1

    def test(self):
        self.assertEqual(STATE.get("L2"), "setup")
