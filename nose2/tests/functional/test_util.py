from __future__ import annotations

from nose2 import util
from nose2.tests._common import TestCase, support_file


class UtilTests(TestCase):
    def test_name_from_path(self):
        test_module = support_file("scenario/tests_in_package/pkg1/test/test_things.py")
        test_package_path = support_file("scenario/tests_in_package")
        self.assertEqual(
            util.name_from_path(test_module),
            ("pkg1.test.test_things", test_package_path),
        )

    def test_non_ascii_output(self):
        class D:
            def __init__(self) -> None:
                self.out: list[str] = []

            def write(self, arg):
                self.out.append(arg)

        stream = D()
        decorated = util._WritelnDecorator(stream)
        string = "\u00dcnic\u00f6de"
        decorated.write(string)
        str("".join(stream.out))
