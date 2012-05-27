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
import logging

from nose2 import events


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
