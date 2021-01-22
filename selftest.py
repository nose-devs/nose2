"""
This is a self-testing wrapper script to run nose2 on itself or, on python2 on Windows,
to modify unittest to run correctly in that context.
"""
import os
import sys

# not windows or running python3 (the "normal" case)
# this variant will respect arguments given on the command line
if os.name != "nt" or sys.version_info >= (3,):
    from nose2 import discover

    discover()

# windows
# this variant discards all command line arguments (because nose2's arguments
# and unittest's CLI arguments are different)
else:
    """
    Python 2.7 Multiprocessing Unittest workaround.
    =====================================================================
    Due the manner in which multiprocessing is handled on windows
    and the fact that __main__.py are actually called __main__

    This workaround bypasses the fact that the calling unittest
    script is called __main__ , but that name won't be discoverable by
    multiprocessing in sys.modules

    http://bugs.python.org/issue10845

    Although fixed in newer python versions, 2.7 has this bug and we must
    therefore account for it.
    """
    from unittest.main import USAGE_AS_MAIN, TestProgram

    class Nose2TestProgram(TestProgram):
        USAGE = USAGE_AS_MAIN

        def __init__(self):
            super(Nose2TestProgram, self).__init__(
                module=None, argv=["unittest", "discover"]
            )

    Nose2TestProgram()
