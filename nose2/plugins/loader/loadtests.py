"""
FIXME docs

"""
from fnmatch import fnmatch
import logging

from nose2 import events, util


log = logging.getLogger(__name__)


class LoadTestsLoader(events.Plugin):
    alwaysOn = True
    configSection = 'load_tests'
    _loading = False

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

    def handleDir(self, event):
        if self._loading:
            return

        if (self._match(event.name, event.pattern) and
            util.ispackage(event.path)):
            name = util.name_from_path(event.path)
            module = util.module_from_name(name)

            load_tests = getattr(module, 'load_tests', None)
            if not load_tests:
                return
            self._loading = True
            try:
                suite = event.loader.suiteClass()
                try:
                    suite = load_tests(event.loader, suite, event.pattern)
                except Exception as exc:
                    log.exception(
                        "Failed to load tests from %s via load_tests", module)
                    suite.addTest(
                        event.loader.failedLoadTests(module.__name__, exc))

                event.handled = True
                return suite
            finally:
                self._loading = False

    def _match(self, filename, pattern):
        return fnmatch(filename, pattern)
