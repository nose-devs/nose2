import logging
import unittest

from pkg2 import get_one

log = logging.getLogger(__name__)
log.debug("module imported")


def test():
    log.debug("test run")
    assert get_one() == 1


def test_fail():
    log.debug("test_fail run")
    assert get_one() == 2


class Tests(unittest.TestCase):
    def test_fail2(self):
        log.debug("test_fail2 run")
        self.assertEqual(get_one(), 4)
