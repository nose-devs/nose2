import sys
import unittest

from nose2 import loader, runner, session
from nose2.main import PluggableTestProgram
__unittest = True


def collector():
    class Test(unittest.TestCase):

        def run(self, result_):
            ok = self._collector(result_)
            sys.exit(not ok)

        def _get_objects(self):
            ssn = session.Session()
            ldr = loader.PluggableTestLoader(ssn)
            rnr = runner.PluggableTestRunner(ssn)
            return ssn, ldr, rnr

        def _collector(self, result_):
            ssn, ldr, rnr = self._get_objects()

            ssn.testLoader = ldr
            ssn.loadConfigFiles('unittest.cfg', 'nose2.cfg', 'setup.cfg')
            ssn.setStartDir()
            ssn.prepareSysPath()
            ssn.loadPlugins(PluggableTestProgram.defaultPlugins)

            test = ldr.loadTestsFromNames([], None)
            rslt = rnr.run(test)
            return rslt.wasSuccessful()

    return Test('_collector')
