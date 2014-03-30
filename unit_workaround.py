"""
Python 2.7 Multiprocessing Unittest workaround.
=====================================================================
Due the manner in which multiprocessing is handled on windows
and the fact that __main__.py are actually called __main__

This workaround bypasses the fact that the calling unittest
script is called __main__

http://bugs.python.org/issue10845

This should be fine for python 3.2+, however, 2.7 and before will
not likely see a fix.  This only affects the unittests called by tox.

Also with python 2.6 , the windows balks on unit2 (the sh script) not 
being a valid executable.
"""
try:
    import unittest2
    from unittest2.main import main, TestProgram, USAGE_AS_MAIN
except ImportError:
    import unittest
    from unittest.main import main, TestProgram, USAGE_AS_MAIN

TestProgram.USAGE = USAGE_AS_MAIN

if __name__ == "__main__":
    main(module=None)

