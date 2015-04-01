"""unittest/unittest2 compatibility wrapper.

Anything internal to nose2 *must* import unittest from here to be
certain that it is using unittest2 when run on older Python versions.

Yes::

  from nose2.compat import unittest

**NO**::

  import unittest

**NO**::

  import unittest2

"""
try:
    import unittest2 as unittest
except ImportError:
    import unittest


try:
    unittest.installHandler
except AttributeError:
    raise ImportError(
        "Built-in unittest version too old; unittest2 is required")

__unittest = True


try:
    from collections import OrderedDict
except ImportError:
    from .backports.ordereddict import OrderedDict
