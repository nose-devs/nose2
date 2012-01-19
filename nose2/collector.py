import sys
import unittest

from nose2 import main, loader, runner, session


def collector():
    class Test(unittest.TestCase):
        def run(self, result_):
            ok = self._collector(result_)
            sys.exit(not ok)

        def _collector(self, result_):
            ssn = session.Session()
            ldr = loader.PluggableTestLoader(ssn)
            rnr = runner.PluggableTestRunner(ssn)

            ssn.loadConfigFiles('unittest.cfg', 'nose2.cfg', 'setup.cfg')
            ssn.prepareSysPath()
            ssn.loadPlugins(main.PluggableTestProgram.defaultPlugins)

            test = ldr.loadTestsFromNames([], None)
            rslt = rnr.run(test)
            return rslt.wasSuccessful()

    return Test('_collector')
