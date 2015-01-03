from nose2.tests._common import TestCase, support_file
from nose2 import util


class UtilTests(TestCase):

    def test_name_from_path(self):
        test_module = support_file('scenario/tests_in_package/pkg1/test/test_things.py')
        test_package_path = support_file('scenario/tests_in_package')
        self.assertEqual(
            util.name_from_path(test_module),
            ('pkg1.test.test_things', test_package_path)
        )
