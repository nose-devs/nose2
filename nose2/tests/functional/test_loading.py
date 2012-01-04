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
from nose2.tests._common import FunctionalTestCase, support_file
from nose2 import util

class TestLoadTestsFromPackage(FunctionalTestCase):
    def test_module_name(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1.test.test_things')
        stdout, stderr = proc.communicate()
        self.assertEqual(proc.poll(), 0, stderr)
        assert 'Ran 16 tests' in util.safe_decode(stderr), stderr

    def test_package_name(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1')
        stdout, stderr = proc.communicate()
        self.assertEqual(proc.poll(), 0, stderr)
        assert 'Ran 16 tests' in util.safe_decode(stderr), stderr

    def test_module_name_with_start_dir(self):
        proc = self.runIn(
            '.', '-v', '-s', support_file('scenario/tests_in_package'),
            'pkg1.test.test_things')
        stdout, stderr = proc.communicate()
        self.assertEqual(proc.poll(), 0, stderr)
        assert 'Ran 16 tests' in util.safe_decode(stderr), stderr

    def test_package_name_with_start_dir(self):
        proc = self.runIn(
            '.', '-v', '-s', support_file('scenario/tests_in_package'), 'pkg1')
        stdout, stderr = proc.communicate()
        self.assertEqual(proc.poll(), 0, stderr)
        assert 'Ran 16 tests' in util.safe_decode(stderr), stderr

    def test_function_name(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1.test.test_things.test_func')
        stdout, stderr = proc.communicate()
        self.assertEqual(proc.poll(), 0, stderr)
        assert 'test_func' in util.safe_decode(stderr), stderr
        assert 'Ran 1 test' in util.safe_decode(stderr), stderr
        assert 'OK' in util.safe_decode(stderr), stderr

    def test_generator_function_name(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1.test.test_things.test_gen')
        stdout, stderr = proc.communicate()
        self.assertEqual(proc.poll(), 0, stderr)
        assert 'test_gen' in util.safe_decode(stderr), stderr
        assert 'Ran 5 tests' in util.safe_decode(stderr), stderr

    def test_generator_function_index(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1.test.test_things.test_gen:3')
        stdout, stderr = proc.communicate()
        self.assertEqual(proc.poll(), 0, stderr)
        assert 'test_gen' in util.safe_decode(stderr), stderr
        assert 'Ran 1 test' in util.safe_decode(stderr), stderr

    def test_generator_function_index_1_based(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1.test.test_things.test_gen:1')
        stdout, stderr = proc.communicate()
        self.assertEqual(proc.poll(), 0, stderr)
        assert 'test_gen' in util.safe_decode(stderr), stderr
        assert 'Ran 1 test' in util.safe_decode(stderr), stderr
        assert 'OK' in util.safe_decode(stderr), stderr

    def test_testcase_name(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1.test.test_things.SomeTests')
        stdout, stderr = proc.communicate()
        self.assertEqual(proc.poll(), 0, stderr)
        assert 'SomeTests' in util.safe_decode(stderr), stderr
        assert 'Ran 4 tests' in util.safe_decode(stderr), stderr

    def test_testcase_method(self):
        proc = self.runIn(
            'scenario/tests_in_package',
            '-v',
            'pkg1.test.test_things.SomeTests.test_ok')
        stdout, stderr = proc.communicate()
        self.assertEqual(proc.poll(), 0, stderr)
        assert 'SomeTests' in util.safe_decode(stderr), stderr
        assert 'Ran 1 test' in util.safe_decode(stderr), stderr
        assert 'OK' in util.safe_decode(stderr), stderr


class TestLoadTestsOutsideOfPackage(FunctionalTestCase):
    def test_module_name(self):
        proc = self.runIn(
            'scenario/package_in_lib',
            '-v',
            'tests')
        stdout, stderr = proc.communicate()
        self.assertEqual(proc.poll(), 0, stderr)
        assert 'Ran 3 tests' in util.safe_decode(stderr), stderr

    def test_function_name(self):
        proc = self.runIn(
            'scenario/package_in_lib',
            '-v',
            'tests.test')
        stdout, stderr = proc.communicate()
        self.assertEqual(proc.poll(), 0, stderr)
        assert 'tests.test' in util.safe_decode(stderr), stderr
        assert 'Ran 1 test' in util.safe_decode(stderr), stderr
        assert 'OK' in util.safe_decode(stderr), stderr

    def test_module_name_with_start_dir(self):
        proc = self.runIn(
            '.', '-v', '-s', support_file('scenario/package_in_lib'), 'tests')
        stdout, stderr = proc.communicate()
        self.assertEqual(proc.poll(), 0, stderr)
        assert 'Ran 3 tests' in util.safe_decode(stderr), stderr
