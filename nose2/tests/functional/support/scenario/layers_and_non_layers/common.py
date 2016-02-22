import unittest
import logging
log = logging.getLogger(__name__)


class UniqueResource(object):
    _instance = None
    used = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(UniqueResource, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def lock(self):
        if not self.used:
            self.used = True
        else:
            raise Exception("Resource allready used")

    def unlock(self):
        if self.used:
            self.used = False
        else:
            raise Exception("Resource already unlocked")


class NormalTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        log.info("Called setUpClass in NormalTest")
        cls.unique_resource = UniqueResource()
        cls.unique_resource.lock()

    @classmethod
    def tearDownClass(cls):
        log.info("Called tearDownClass in NormalTest")
        cls.unique_resource.unlock()

    def test(self):
        self.assertTrue(self.unique_resource.used)


class NormalTestTwo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        log.info("Called setUpClass in NormalTestTwo")
        cls.unique_resource = UniqueResource()
        cls.unique_resource.lock()

    @classmethod
    def tearDownClass(cls):
        log.info("Called tearDownClass in NormalTestTwo")
        cls.unique_resource.unlock()

    def test(self):
        self.assertTrue(self.unique_resource.used)
