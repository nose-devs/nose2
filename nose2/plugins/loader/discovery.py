"""
Adapted from unittest2/loader.py from the unittest2 plugins branch.

This module contains some code copied from unittest2/loader.py and other
code developed in reference to that module and others within unittest2.

unittest2 is Copyright (c) 2001-2010 Python Software Foundation; All
Rights Reserved. See: http://docs.python.org/license.html

"""
from fnmatch import fnmatch
import os
import sys

from nose2 import events, util


class DiscoveryLoader(events.Plugin):

    def __init__(self):
        self.start_dir = None
        self.top_level_dir = self.start_dir
        self._top_level_dir = None # ???

        self.addOption(
            self.setStartDir,
            'S', 'start-directory', "Directory to start discovery ('.' default)")
        self.addOption(
            self.setTopLevelDir,
            'T', 'top-level-directory',
            "Top level directory of project (defaults to start dir)")
        # really always on!
        self.register()

    def setStartDir(self, start_dir):
        self.start_dir = start_dir

    def setTopLevelDir(self, top_level_dir):
        self.top_level_dir = top_level_dir

    def createTests(self, event):
        event.handled = True # I'm taking this one
        return self.discover(event, self.start_dir, self.top_level_dir)

    def discover(self, event, start_dir, top_level_dir):
        print "** discover", start_dir, top_level_dir
        loader = event.loader
        pattern = self.session.testFilePattern
        implicit_start = False
        if start_dir is None:
            start_dir = '.'
            implicit_start = True
        set_implicit_top = False
        if top_level_dir is None and self._top_level_dir is not None:
            # make top_level_dir optional if called from load_tests in a package
            top_level_dir = self._top_level_dir
        elif top_level_dir is None:
            set_implicit_top = True
            top_level_dir = start_dir

        top_level_dir = os.path.abspath(top_level_dir)

        if not top_level_dir in sys.path:
            # all test modules must be importable from the top level directory
            # should we *unconditionally* put the start directory in first
            # in sys.path to minimise likelihood of conflicts between installed
            # modules and development versions?
            sys.path.insert(0, top_level_dir)
        self._top_level_dir = top_level_dir

        is_not_importable = False
        if os.path.isdir(os.path.abspath(start_dir)):
            start_dir = os.path.abspath(start_dir)
            if start_dir != top_level_dir:
                is_not_importable = not os.path.isfile(
                    os.path.join(start_dir, '__init__.py'))
        else:
            # support for discovery from dotted module names
            try:
                __import__(start_dir)
            except ImportError:
                is_not_importable = True
            else:
                the_module = sys.modules[start_dir]
                top_part = start_dir.split('.')[0]
                start_dir = os.path.abspath(
                    os.path.dirname((the_module.__file__)))
                if set_implicit_top:
                    self._top_level_dir = os.path.abspath(
                        os.path.dirname(
                            os.path.dirname(sys.modules[top_part].__file__)))
                    sys.path.remove(top_level_dir)

        if is_not_importable:
            raise ImportError(
                'Start directory is not importable: %r' % start_dir)

        def check_dir(the_dir):
            if not implicit_start:
                return
            full_path =  os.path.join(start_dir, the_dir)
            if (os.path.isdir(full_path) and not
                os.path.isfile(os.path.join(full_path, '__init__.py'))):
                sys.path.append(full_path)
                return full_path

        src_dir = check_dir('src')
        lib_dir = check_dir('lib')
        tests = list(self._find_tests(event, start_dir, pattern))
        real_top_level = self._top_level_dir
        if lib_dir is not None:
            self._top_level_dir = lib_dir
            tests.extend(list(self._find_tests(event, lib_dir, pattern)))
        if src_dir is not None:
            self._top_level_dir = src_dir
            tests.extend(list(self._find_tests(event, src_dir, pattern)))
        if implicit_start:
            for entry in os.listdir(start_dir):
                if not 'test' in entry.lower():
                    continue
                full = check_dir(entry)
                if full is None:
                    continue
                self._top_level_dir = full
                tests.extend(list(self._find_tests(event, full, pattern)))

        self._top_level_dir = real_top_level
        return loader.suiteClass(tests)

    def _find_tests(self, event, start_dir, pattern):
        """Used by discovery. Yields test suites it loads."""
        paths = os.listdir(start_dir)

        for path in paths:
            full_path = os.path.join(start_dir, path)
            if os.path.isfile(full_path):
                evt = events.HandleFileEvent(self, path, full_path, pattern,
                                             self._top_level_dir)
                result = self.session.hooks.handleFile(evt)
                if evt.extraTests:
                    yield self.suiteClass(evt.extraTests)

                if evt.handled:
                    if result:
                        yield result
                    continue

                if not util.valid_module_name(path):
                    # valid Python identifiers only
                    continue

                evt = events.MatchPathEvent(path, full_path, pattern)
                result = self.session.hooks.matchPath(evt)
                if evt.handled:
                    if not result:
                        continue
                elif not self._match_path(path, full_path, pattern):
                    continue

                # if the test file matches, load it
                name = util.name_from_path(full_path)
                try:
                    module = util.module_from_name(name)
                except:
                    yield event.loader.failedImport(name)
                else:
                    mod_file = os.path.abspath(
                        getattr(module, '__file__', full_path))
                    realpath = os.path.splitext(mod_file)[0]
                    fullpath_noext = os.path.splitext(full_path)[0]
                    if realpath.lower() != fullpath_noext.lower():
                        module_dir = os.path.dirname(realpath)
                        mod_name = os.path.splitext(os.path.basename(full_path))[0]
                        expected_dir = os.path.dirname(full_path)
                        msg = ("%r module incorrectly imported from %r. "
                               "Expected %r. Is this module globally installed?"
                               )
                        raise ImportError(
                            msg % (mod_name, module_dir, expected_dir))
                    yield event.loader.loadTestsFromModule(module)
            elif os.path.isdir(full_path):
                if not os.path.isfile(os.path.join(full_path, '__init__.py')):
                    continue

                load_tests = None
                tests = None
                if fnmatch(path, pattern):
                    # only check load_tests if the package directory
                    # itself matches the filter
                    name = util.name_from_path(full_path)
                    package = util.module_from_name(name)
                    load_tests = getattr(package, 'load_tests', None)
                    tests = event.loader.loadTestsFromModule(
                        package, use_load_tests=False)

                if load_tests is None:
                    if tests is not None:
                        # tests loaded from package file
                        yield tests
                    # recurse into the package
                    for test in self._find_tests(event, full_path, pattern):
                        yield test
                else:
                    try:
                        yield load_tests(self, tests, pattern)
                    except Exception, e:
                        yield event.loader.failedLoadTests(
                            package.__name__, e)

    def _match_path(self, path, full_path, pattern):
        # override this method to use alternative matching strategy
        return fnmatch(path, pattern)
