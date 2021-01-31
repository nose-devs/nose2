import unittest


class Case(unittest.TestCase):
    def test_subtest_success(self):
        for i in range(3):
            with self.subTest(i=i):
                self.assertTrue(i < 3)

    def test_subtest_failure(self):
        for i in range(6):
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)

    def test_subtest_error(self):
        for i in range(3):
            with self.subTest(i=i):
                raise RuntimeError(i)

    @unittest.expectedFailure
    def test_subtest_expected_failure(self):
        for i in range(6):
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)

    def test_subtest_message(self):
        for i in range(6):
            with self.subTest("msg", i=i):
                self.assertEqual(i % 2, 0)
