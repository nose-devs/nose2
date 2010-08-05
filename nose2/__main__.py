"""Main entry point"""

import sys
if sys.argv[0].endswith("__main__.py"):
    sys.argv[0] = "nose2"

__unittest = True

from nose2.main import main_
main_()
