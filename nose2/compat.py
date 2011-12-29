try:
    import unittest2 as unittest
except ImportError:
    import unittest


try:
    unittest.installHandler
except AttributeError:
    raise ImportError("Built-in unittest version too old, unittest2 is required")
