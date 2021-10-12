import logging
import unittest

import nose2

log = logging.getLogger(__name__)


class Test(unittest.TestCase):
    def test_logging_keeps_copies_of_mutable_objects(self):
        d = {}
        log.debug("foo: %s", d)
        d["bar"] = "baz"
        self.assertTrue(False)


if __name__ == "__main__":
    nose2.main()
