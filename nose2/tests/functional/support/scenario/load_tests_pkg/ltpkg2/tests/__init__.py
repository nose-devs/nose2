import unittest


def load_tests(loader, standard_tests, pattern):
    suite = loader.suiteClass()

    class Test(unittest.TestCase):
        def test(self):
            import ltpkg2

            assert ltpkg2.lt(1, 2)

    suite.addTest(Test("test"))
    return suite
