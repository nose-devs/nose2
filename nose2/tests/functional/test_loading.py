"""
pkg1
pkg1.test
pkg1.test.test_things
pkg1.test.test_things.test_func
pkg1.test.test_things.test_gen
pkg1.test.test_things.test_gen:3
pkg1.test.test_things.SomeTests
pkg1.test.test_things.SomeTests.test_ok

# generator method
# generator method index

# param func
# param func index
# param method
# param method index

"""
import sys
from nose2.tests._common import FunctionalTestCase, support_file


class TestLoadTestsFromPackage(FunctionalTestCase):

    def test_start_directory_inside_package(self):
        proc = self.runIn(
            'scenario/tests_in_package/pkg1/test',
            '-v',
            '-t',
            support_file('scenario/tests_in_package'))
        self.assertTestRunOutputMatches(proc, stderr='Ran 25 tests')
        self.assertEqual(proc.poll(), 1)

    def test_project_directory_inside_package(self):
        proc = self.runIn(
            'scenario/tests_in_package/pkg1/test',
            '-v')
        self.assertTestRunOutputMatches(proc, stderr='Ran 25 tests')
        self.assertEqual(proc.poll(), 1)

    def test_module_name(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1.test.test_things')
        self.assertTestRunOutputMatches(proc, stderr='Ran 25 tests')
        self.assertEqual(proc.poll(), 1)

    def test_package_name(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1')
        self.assertTestRunOutputMatches(proc, stderr='Ran 25 tests')
        self.assertEqual(proc.poll(), 1)

    def test_module_name_with_start_dir(self):
        proc = self.runIn(
            '.', '-v', '-s', support_file('scenario/tests_in_package'),
            'pkg1.test.test_things')

        self.assertTestRunOutputMatches(proc, stderr='Ran 25 tests')
        self.assertEqual(proc.poll(), 1)

    def test_package_name_with_start_dir(self):
        proc = self.runIn(
            '.', '-v', '-s', support_file('scenario/tests_in_package'), 'pkg1')
        self.assertTestRunOutputMatches(proc, stderr='Ran 25 tests')
        self.assertEqual(proc.poll(), 1)

    def test_function_name(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1.test.test_things.test_func')
        self.assertTestRunOutputMatches(
            proc, stderr='test_func')
        self.assertTestRunOutputMatches(
            proc, stderr='Ran 1 test')
        self.assertTestRunOutputMatches(
            proc, stderr='OK')
        self.assertEqual(proc.poll(), 0)

    def test_generator_function_name(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1.test.test_things.test_gen')
        self.assertTestRunOutputMatches(proc, stderr='test_gen')
        self.assertTestRunOutputMatches(proc, stderr='Ran 5 tests')
        self.assertEqual(proc.poll(), 0)

    def test_generator_function_index(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1.test.test_things.test_gen:3')
        self.assertTestRunOutputMatches(proc, stderr='test_gen')
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertEqual(proc.poll(), 0)

    def test_generator_function_index_1_based(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1.test.test_things.test_gen:1')

        self.assertTestRunOutputMatches(proc, stderr='test_gen')
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertTestRunOutputMatches(proc, stderr='OK')
        self.assertEqual(proc.poll(), 0)

    def test_testcase_name(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1.test.test_things.SomeTests')
        self.assertTestRunOutputMatches(proc, stderr='SomeTests')
        self.assertTestRunOutputMatches(proc, stderr='Ran 8 tests')
        self.assertEqual(proc.poll(), 1)

    def test_testcase_method(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1.test.test_things.SomeTests.test_ok')
        self.assertTestRunOutputMatches(proc, stderr='SomeTests')
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertTestRunOutputMatches(proc, stderr='OK')
        self.assertEqual(proc.poll(), 0)

    def test_generator_method(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1.test.test_things.SomeTests.test_gen_method')
        self.assertTestRunOutputMatches(proc, stderr='test_gen_method')
        self.assertTestRunOutputMatches(proc, stderr='Ran 2 tests')
        self.assertEqual(proc.poll(), 1)

    def test_generator_method_index(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1.test.test_things.SomeTests.test_gen_method:1')
        self.assertTestRunOutputMatches(proc, stderr='test_gen_method')
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertTestRunOutputMatches(proc, stderr='OK')
        self.assertEqual(proc.poll(), 0)

    def test_parameterized_method(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1.test.test_things.SomeTests.test_params_method')
        self.assertTestRunOutputMatches(proc, stderr='test_params_method')
        self.assertTestRunOutputMatches(proc, stderr='Ran 2 tests')
        self.assertEqual(proc.poll(), 1)

    def test_parameterized_method_index(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1.test.test_things.SomeTests.test_params_method:1')
        self.assertTestRunOutputMatches(proc, stderr='test_params_method')
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertTestRunOutputMatches(proc, stderr='OK')
        self.assertEqual(proc.poll(), 0)

    def test_parameterized_func(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1.test.test_things.test_params_func')
        self.assertTestRunOutputMatches(proc, stderr='test_params_func')
        self.assertTestRunOutputMatches(proc, stderr='Ran 2 tests')
        self.assertEqual(proc.poll(), 1)

    def test_parameterized_func_index(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1.test.test_things.test_params_func:1')
        self.assertTestRunOutputMatches(proc, stderr='test_params_func')
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertTestRunOutputMatches(proc, stderr='OK')
        self.assertEqual(proc.poll(), 0)


class TestLoadTestsOutsideOfPackage(FunctionalTestCase):

    def test_module_name(self):
        proc = self.runIn(
            'scenario/package_in_lib',
            '-v',
            'tests')
        self.assertTestRunOutputMatches(proc, stderr='Ran 3 tests')
        self.assertEqual(proc.poll(), 1)

    def test_function_name(self):
        proc = self.runIn(
            'scenario/package_in_lib',
            '-v',
            'tests.test')
        self.assertTestRunOutputMatches(proc, stderr='test')
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertTestRunOutputMatches(proc, stderr='OK')
        self.assertEqual(proc.poll(), 0)

    def test_module_name_with_start_dir(self):
        proc = self.runIn(
            '.', '-v', '-s', support_file('scenario/package_in_lib'), 'tests')
        self.assertTestRunOutputMatches(proc, stderr='Ran 3 tests')
        self.assertEqual(proc.poll(), 1)


class TestLoadingErrors(FunctionalTestCase):

    def test_import_error_module(self):
        proc = self.runIn(
            'scenario/module_import_err',
            '-v',
            'test_import_err')
        self.assertTestRunOutputMatches(proc, stderr='ImportError: booms')
        self.assertTestRunOutputMatches(proc, stderr='Traceback \(most recent call last\):')
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertEqual(proc.poll(), 1)

    def test_import_error_func(self):
        proc = self.runIn(
            'scenario/module_import_err',
            '-v',
            'test_import_err.test')
        self.assertTestRunOutputMatches(proc, stderr='ImportError: booms')
        self.assertTestRunOutputMatches(proc, stderr='Traceback \(most recent call last\):')
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertEqual(proc.poll(), 1)

    def test_import_error_testcase(self):
        proc = self.runIn(
            'scenario/module_import_err',
            '-v',
            'test_import_err.Test')
        self.assertTestRunOutputMatches(proc, stderr='ImportError: booms')
        self.assertTestRunOutputMatches(proc, stderr='Traceback \(most recent call last\):')
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertEqual(proc.poll(), 1)

    def test_import_error_testcase_method(self):
        proc = self.runIn(
            'scenario/module_import_err',
            '-v',
            'test_import_err.Test.test')
        self.assertTestRunOutputMatches(proc, stderr='ImportError: booms')
        self.assertTestRunOutputMatches(proc, stderr='Traceback \(most recent call last\):')
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertEqual(proc.poll(), 1)

    def test_import_error_package(self):
        proc = self.runIn(
            'scenario/module_import_err',
            '-v',
            'pkg')
        # In this case, there should not be an AttributeError since we only
        # import pkg, which should work.
        self.assertTestRunOutputMatches(proc, stderr='ImportError: Failed to import test module: pkg.test_import_err')
        self.assertTestRunOutputMatches(proc, stderr='Traceback \(most recent call last\):')
        self.assertTestRunOutputMatches(proc, stderr='ValueError: booms')
        # 3 tests should run, and only one should fail. We're testing that a
        # loading error does not prevent from running other tests.
        self.assertTestRunOutputMatches(proc, stderr='Ran 3 tests')
        self.assertTestRunOutputMatches(proc, stderr='FAILED \(errors=1\)')
        self.assertEqual(proc.poll(), 1)

    def test_import_error_module_in_package(self):
        proc = self.runIn(
            'scenario/module_import_err',
            '-v',
            'pkg.test_import_err')
        # In this case, there should not be an ImportError. The import of
        # pkg.test_import_err fails due with a `ValueError`, and this is the
        # one we are expecting.
        self.assertTestRunOutputMatches(proc, stderr='AttributeError: ')
        self.assertTestRunOutputMatches(proc, stderr='ValueError: booms')
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertEqual(proc.poll(), 1)

    def test_import_error_unknown_module_in_package(self):
        proc = self.runIn(
            'scenario/module_import_err',
            '-v',
            'pkg.test_does_not_exit')
        # In this case, there should not be an ImportError. The import of
        # pkg.test_import_err fails due with a `ValueError`, and this is the
        # one we are expecting.
        self.assertTestRunOutputMatches(proc, stderr='AttributeError: ')

        # py3.6 introduced ModuleNotFoundError, a subclass of ImportError
        if sys.version_info < (3, 6):
            importerr = 'ImportError: No module named'
        else:
            importerr = 'ModuleNotFoundError: No module named'
        self.assertTestRunOutputMatches(proc, stderr=importerr)

        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertEqual(proc.poll(), 1)



class TestTestClassLoading(FunctionalTestCase):

    def test_load_testclass_by_name(self):
        proc = self.runIn(
            'scenario/test_classes',
            '-v',
            'test_classes.Test')
        self.assertTestRunOutputMatches(proc, stderr='Ran 8 tests')
        self.assertEqual(proc.poll(), 0)

    def test_load_testclass_method_by_name(self):
        proc = self.runIn(
            'scenario/test_classes',
            '-v',
            'test_classes.Test.test')
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertEqual(proc.poll(), 0)

    def test_load_testclass_generator_method_by_name(self):
        proc = self.runIn(
            'scenario/test_classes',
            '-v',
            'test_classes.Test.test_gen')
        self.assertTestRunOutputMatches(proc, stderr='Ran 5 tests')
        self.assertEqual(proc.poll(), 0)

    def test_load_testclass_params_method_by_name(self):
        proc = self.runIn(
            'scenario/test_classes',
            '-v',
            'test_classes.Test.test_params')
        self.assertTestRunOutputMatches(proc, stderr='Ran 2 tests')
        self.assertEqual(proc.poll(), 0)

    def test_class_level_fixtures_supported(self):
        proc = self.runIn(
            'scenario/test_classes',
            '-v',
            'test_fixtures')
        self.assertTestRunOutputMatches(proc, stderr='Ran 5 tests')
        self.assertEqual(proc.poll(), 0)

    def test_error_in_test_class(self):
        proc = self.runIn(
            'scenario/test_class_fail',
            '-v',
            'test_class_fail')
        self.assertTestRunOutputMatches(proc, stderr='nose2.loader.LoadTestsFailure')
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertTestRunOutputMatches(proc, stderr='FAILED')
        self.assertEqual(proc.poll(), 1)

    def test_expected_failures(self):
        proc = self.runIn(
            'scenario/expected_failures',
            '-v',
            'expected_failures')
        self.assertTestRunOutputMatches(proc, stderr=r'FAILED \(failures=1, expected failures=1, unexpected successes=1\)')

