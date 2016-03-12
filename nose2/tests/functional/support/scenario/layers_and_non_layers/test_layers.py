import unittest
import logging
from .common import UniqueResource, NormalTest, NormalTestTwo
log = logging.getLogger(__name__)


class Layer1(object):

    @classmethod
    def setUp(cls):
        log.info("Called setup in layer 1")
        cls.unique_resource = UniqueResource()
        cls.unique_resource.lock()

    @classmethod
    def tearDown(cls):
        log.info("Called teardown in layer 2")
        cls.unique_resource.unlock()


class Layer2(object):

    @classmethod
    def setUp(cls):
        log.info("Called setup in layer 2")
        cls.unique_resource = UniqueResource()
        cls.unique_resource.lock()

    @classmethod
    def tearDown(cls):
        log.info("Called teardown in layer 2")
        cls.unique_resource.unlock()


class Layer3(Layer2):

    @classmethod
    def setUp(cls):
        log.info("Called setup in layer 3")

    @classmethod
    def tearDown(cls):
        log.info("Called teardown in layer 3")


class LayerTest1(unittest.TestCase):

    layer = Layer1

    def test(self):
        self.assertTrue(self.layer.unique_resource.used)


class LayerTest2(unittest.TestCase):

    layer = Layer2

    def test(self):
        self.assertTrue(self.layer.unique_resource.used)


class LayerTest3(unittest.TestCase):

    layer = Layer2

    def test(self):
        self.assertTrue(self.layer.unique_resource.used)
