import nose2
import unittest
import logging

log = logging.getLogger(__name__)


class Test(unittest.TestCase):

    def test_logging_config(self):
        log.debug("foo")
        log.info("bar")
        assert False


if __name__ == '__main__':
    nose2.main()
