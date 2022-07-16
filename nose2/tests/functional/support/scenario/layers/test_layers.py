import unittest

STATE = {}


class Base:
    @classmethod
    def setUp(cls):
        STATE["base"] = "setup"

    @classmethod
    def tearDown(cls):
        del STATE["base"]


class LayerA(Base):
    position = 1

    @classmethod
    def setUp(cls):
        STATE["layerA"] = "setup"

    @classmethod
    def tearDown(cls):
        del STATE["layerA"]

    @classmethod
    def testSetUp(cls, test):
        STATE["layerA.test"] = "setup"
        # print "->", STATE, test

    @classmethod
    def testTearDown(cls, test):
        # print "<-", STATE, test
        del STATE["layerA.test"]


class LayerA_1(LayerA):
    position = 0

    @classmethod
    def setUp(cls):
        STATE["layerA_1"] = "setup"

    @classmethod
    def tearDown(cls):
        del STATE["layerA_1"]


class LayerB(LayerA):
    position = 2

    @classmethod
    def setUp(cls):
        STATE["layerB"] = "setup"

    @classmethod
    def tearDown(cls):
        del STATE["layerB"]


class LayerB_1(LayerB):
    position = 0

    @classmethod
    def setUp(cls):
        STATE["layerB_1"] = "setup"

    @classmethod
    def tearDown(cls):
        del STATE["layerB_1"]


class LayerC(LayerB, LayerA):
    position = 1

    @classmethod
    def setUp(cls):
        STATE["layerC"] = "setup"

    @classmethod
    def tearDown(cls):
        del STATE["layerC"]


class LayerD(Base):
    position = 0

    @classmethod
    def setUp(cls):
        STATE["layerD"] = "setup"

    @classmethod
    def tearDown(cls):
        del STATE["layerD"]


class Outer(unittest.TestCase):
    layer = Base

    def test(self):
        self.assertEqual(STATE.get("base"), "setup")


class InnerA(unittest.TestCase):
    layer = LayerA

    def setUp(self):
        STATE["innerA.test"] = "setup"

    def tearDown(self):
        del STATE["innerA.test"]

    def test(self):
        expect = {
            "base": "setup",
            "layerA": "setup",
            "innerA.test": "setup",
            "layerA.test": "setup",
        }
        for k, v in expect.items():
            self.assertEqual(STATE.get(k), v)


class InnerA_1(unittest.TestCase):
    layer = LayerA_1

    def test(self):
        expect = {
            "base": "setup",
            "layerA": "setup",
            "layerA_1": "setup",
            "layerA.test": "setup",
        }
        for k, v in expect.items():
            self.assertEqual(STATE.get(k), v)


class InnerB(unittest.TestCase):
    layer = LayerB

    def setUp(self):
        STATE["innerB.test"] = "setup"

    def tearDown(self):
        STATE["innerB.test"] = "tearDown"


class InnerB_1(unittest.TestCase):
    layer = LayerB_1

    def test(self):
        expect = {"base": "setup", "layerB": "setup", "layerB_1": "setup"}
        for k, v in expect.items():
            self.assertEqual(STATE.get(k), v)


class InnerC(unittest.TestCase):
    layer = LayerC

    def test(self):
        expect = {
            "base": "setup",
            "layerB": "setup",
            "layerC": "setup",
            "layerA": "setup",
            "layerA.test": "setup",
        }
        for k, v in expect.items():
            self.assertEqual(STATE.get(k), v)

    def test2(self):
        expect = {
            "base": "setup",
            "layerB": "setup",
            "layerC": "setup",
            "layerA": "setup",
            "layerA.test": "setup",
        }
        for k, v in expect.items():
            self.assertEqual(STATE.get(k), v)


class InnerD(unittest.TestCase):
    layer = LayerD

    def test(self):
        """test with docstring"""
        self.assertEqual({"base": "setup", "layerD": "setup"}, STATE)


class NoLayer(unittest.TestCase):
    def test(self):
        self.assertEqual(STATE, {})
