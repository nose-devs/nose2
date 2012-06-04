"""

FIXME support load_tests protocol

                load_tests = None
                tests = None
                if fnmatch(path, pattern):
                    # only check load_tests if the package directory
                    # itself matches the filter
                    name = util.name_from_path(entry_path)
                    package = util.module_from_name(name)
                    load_tests = getattr(package, 'load_tests', None)
                    tests = loader.loadTestsFromModule(
                        package, useLoadTests=False)

                if load_tests is None:
                    if tests is not None:
                        # tests loaded from package file
                        yield tests
                    # recurse into the package
                else:
                    try:
                        yield load_tests(self, tests, pattern)
                    except Exception:
                        ec, ev, tb = sys.exec_info()
                        yield loader.failedLoadTests(
                            package.__name__, ev)


"""
from fnmatch import fnmatch
import logging
import os

from nose2 import events, util


log = logging.getLogger(__name__)


class LoadTestsLoader(events.Plugin):
    alwaysOn = True
    configSection = 'load_tests'

    def registerInSubprocess(self, event):
        event.pluginClasses.append(self.__class__)

    def moduleLoadedSuite(self, event):
        module = event.module
        load_tests = getattr(module, 'load_tests', None)
        if not load_tests:
            return
        try:
            event.suite = load_tests(
                event.loader, event.suite, self.session.testFilePattern)
        except Exception as exc:
            log.exception("Failed to load tests from %s via load_tests", module)
            suite = event.loader.suiteClass()
            suite.addTest(event.loader.failedLoadTests(module.__name__, exc))
            event.handled = True
            return suite

    def matchDirPath(self, event):
        # if pattern matches, and dir is package
        # try importing package. if package contains load_tests
        # return false and set event.handled
        if (self._match(event.name, event.pattern) and
            util.ispackage(event.path)):
            name = util.name_from_path(event.path)
            module = util.module_from_name(name)
            if hasattr(module, 'load_tests'):
                event.handled = True
                return False

    def matchPatch(self, event):
        # if filename is __init__ and package part matches
        # test pattern then return true and set event.handled
        if (event.name == '__init__.py' and
            self._match(os.path.basename(os.path.dirname(event.path)),
                        event.pattern)):
            event.handled = True
            return True

    def _match(self, filename, pattern):
        return fnmatch(filename, pattern)
