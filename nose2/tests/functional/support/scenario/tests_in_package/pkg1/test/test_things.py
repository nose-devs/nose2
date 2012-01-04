import unittest


class SomeTests(unittest.TestCase):

    def test_ok(self):
        pass

    def test_typeerr(self):
        raise TypeError("oops")

    def test_failed(self):
        print("Hello stdout")
        assert False, "I failed"

    def test_skippy(self):
        raise unittest.SkipTest("I wanted to skip")

    def test_gen_method(self):
        def check(x):
            assert x == 1
        yield check, 1
        yield check, 2

    def test_params_method(self, a):
        self.assertEqual(a, 1)
    test_params_method.paramList = (1, 2)


def test_func():
    assert 1 == 1


def test_gen():
    def check(a, b):
        assert a == b
    for i in range(0, 5):
        yield check, (i, i,)
test_gen.testGenerator = True


def test_gen_nose_style():
    def check(a, b):
        assert a == b
    for i in range(0, 5):
        yield check, i, i


did_setup = False
def setup():
    global did_setup
    did_setup = True


def test_fixt():
    assert did_setup
test_fixt.setup = setup


def test_params_func(a):
    assert a == 1
test_params_func.paramList = (1, 2)


def test_params_func_multi_arg(a, b):
    assert a == b
test_params_func_multi_arg.paramList = ((1, 1), (1, 2), (2, 2))
