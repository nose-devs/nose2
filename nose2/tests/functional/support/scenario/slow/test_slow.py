import logging
import time
import unittest

log = logging.getLogger(__name__)


class TestSlow(unittest.TestCase):
    def test_ok(self):
        print("hide this")
        time.sleep(2)

    def test_fail(self):
        print("show this")
        log.debug("hola")
        time.sleep(2)
        self.assertEqual(1, 2)

    def test_err(self):
        print("show this too")
        log.debug("ciao")
        time.sleep(2)
        {}["x"]
