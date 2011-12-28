import unittest2

class SomeTests(unittest2.TestCase):

    def test_ok(self):
        pass

    def test_typeerr(self):
        raise TypeError("oops")

    def test_failed(self):
        print "Hello stdout"
        assert False, "I failed"

    def test_skippy(self):
        raise unittest2.SkipTest("I wanted to skip")


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

