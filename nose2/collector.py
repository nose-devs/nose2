import os
import sys
import unittest

from nose2 import events, loader, runner, session
from nose2.main import PluggableTestProgram

__unittest = True


def collector():
    """
    This is the entry point used by setuptools, as in::

      python setup.py test

    """

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
            ssn.loadConfigFiles(
                "unittest.cfg",
                "nose2.cfg",
                "setup.cfg",
                os.path.expanduser("~/.unittest.cfg"),
                os.path.expanduser("~/.nose2.cfg"),
            )
            ssn.setStartDir()
            ssn.prepareSysPath()
            ssn.loadPlugins(PluggableTestProgram.defaultPlugins)

            # TODO: refactor argument parsing to make it possible to feed CLI
            # args to plugins via this path (currently done in
            # PluggableTestProgram)
            # in order to do this, it seems like features in
            # PluggableTestProgram need to be factored out into some source
            # from which both it and this dummy test case can invoke them
            #
            # this is the disabled feature:
            # ssn.hooks.handleArgs(events.CommandLineArgsEvent(...))
            #
            # this means that there may be plugins which don't work under
            # setuptools invocation because they expect to get handleArgs
            # triggered (e.g. older versions of the coverage plugin)

            # FIXME: this is all a great-big DRY violation when compared with
            # PluggableTestProgram

            # create the testsuite, and make sure the createTests event gets
            # triggered, as some plugins expect it
            # just doing `ldr.loadTestsFromNames` works, but leaves some
            # plugins in the lurch
            event = events.CreateTestsEvent(ldr, [], None)
            result = ssn.hooks.createTests(event)
            if event.handled:
                test = event
            else:
                test = ldr.loadTestsFromNames([], None)

            # fire the "createdTestSuite" event for plugins to handle
            # as above, we can get away without this, but some plugins will
            # expect it
            event = events.CreatedTestSuiteEvent(test)
            result = ssn.hooks.createdTestSuite(event)
            if event.handled:
                test = result

            rslt = rnr.run(test)
            return rslt.wasSuccessful()

    return Test("_collector")
