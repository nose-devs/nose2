import unittest


class SomeTests(unittest.TestCase):
    tags = ["case"]

    def test_ok(self):
        pass

    test_ok.tags = ["method", "pass"]  # type: ignore[attr-defined]
    test_ok.a = 0  # type: ignore[attr-defined]
    test_ok.b = 1  # type: ignore[attr-defined]

    def test_typeerr(self):
        raise TypeError("oops")

    test_typeerr.tags = ["method"]  # type: ignore[attr-defined]

    def test_failed(self):
        print("Hello stdout")
        assert False, "I failed"

    test_failed.tags = ["method"]  # type: ignore[attr-defined]

    def test_skippy(self):
        raise unittest.SkipTest("I wanted to skip")

    test_skippy.a = 1  # type: ignore[attr-defined]
    test_skippy.b = 1  # type: ignore[attr-defined]

    def test_gen_method(self):
        def check(x):
            assert x == 1

        check.b = 2  # type: ignore[attr-defined]
        yield check, 1
        yield check, 2

    test_gen_method.a = 1  # type: ignore[attr-defined]
    test_gen_method.b = 1  # type: ignore[attr-defined]

    def test_params_method(self, a):
        self.assertEqual(a, 1)

    test_params_method.paramList = (1, 2)  # type: ignore[attr-defined]
    test_params_method.a = 1  # type: ignore[attr-defined]


def test_func():
    assert 1 == 1


test_func.a = 1  # type: ignore[attr-defined]
test_func.b = 0  # type: ignore[attr-defined]
test_func.tags = ["func", "pass"]  # type: ignore[attr-defined]


def test_gen():
    def check(a, b):
        assert a == b

    check.tags = ["func"]  # type: ignore[attr-defined]
    for i in range(0, 5):
        yield check, (i, i)


test_gen.testGenerator = True  # type: ignore[attr-defined]
test_gen.tags = ["func"]  # type: ignore[attr-defined]


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


test_fixt.setup = setup  # type: ignore[attr-defined]


def test_params_func(a):
    assert a == 1


test_params_func.paramList = (1, 2)  # type: ignore[attr-defined]
test_params_func.tags = ["func"]  # type: ignore[attr-defined]


def test_params_func_multi_arg(a, b):
    assert a == b


test_params_func_multi_arg.paramList = ((1, 1), (1, 2), (2, 2))  # type: ignore[attr-defined]  # noqa: E501
