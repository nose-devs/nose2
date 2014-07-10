# -*- coding: utf-8 -*-
import six

from nose2.tests._common import TestCase, support_file
from nose2 import util


class UtilTests(TestCase):

    def test_name_from_path(self):
        self.assertEqual(
            util.name_from_path(support_file('scenario/tests_in_package/pkg1/test/test_things.py')), 'pkg1.test.test_things')

    def test_non_ascii_output(self):
        class D:
            def __init__(self):
                self.out = []
            def write(self, arg):
                self.out.append(arg)

        stream = D()
        decorated = util._WritelnDecorator(stream)
        string = six.u('\u00dcnic\u00f6de')
        decorated.write(string)
        # fails on py2 if output is not properly encoded
        str("".join(stream.out))
