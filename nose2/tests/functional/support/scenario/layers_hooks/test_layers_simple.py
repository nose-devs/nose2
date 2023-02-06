import unittest


class Layer1:
    layer_setup = 0
    test_setup = 0
    test_teardown = 0
    layer_teardown = 0
    tests_count = 0

    @classmethod
    def setUp(cls):
        if cls.layer_setup >= 1:
            raise Exception("layer_setup already ran")
        cls.layer_setup += 1

    @classmethod
    def testSetUp(cls):
        if cls.test_setup >= 2:
            raise Exception("test_setup already ran twice")
        cls.test_setup += 1

    @classmethod
    def testTearDown(cls):
        if cls.test_teardown >= 2:
            raise Exception("test_teardown already ran twice")
        cls.test_teardown += 1

    @classmethod
    def tearDown(cls):
        if cls.layer_teardown >= 1:
            raise Exception("layer_teardown already ran")
        cls.layer_teardown += 1


class TestSimple(unittest.TestCase):
    layer = Layer1

    def test_1(self):
        assert self.layer.layer_setup == 1
        assert self.layer.test_setup == self.layer.tests_count + 1
        assert self.layer.test_teardown == self.layer.tests_count
        assert self.layer.layer_teardown == 0
        self.layer.tests_count += 1

    def test_2(self):
        assert self.layer.layer_setup == 1
        assert self.layer.test_setup == self.layer.tests_count + 1
        assert self.layer.test_teardown == self.layer.tests_count
        assert self.layer.layer_teardown == 0
        self.layer.tests_count += 1
