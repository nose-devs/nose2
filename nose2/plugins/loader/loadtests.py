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
