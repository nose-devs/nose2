import time

from nose2.tools import such


def slow_blocking_init():
    print("YEAH2")
    time.sleep(1)
    print("a second elapsed")
    time.sleep(1)
    print("a second elapsed")
    return True


class Layer1:
    description = "Layer1 description"

    @classmethod
    def setUp(cls):
        print("YEAH")
        it.obj = False


class Layer2:
    description = "Layer2 description"

    @classmethod
    def setUp(cls):
        it.obj = slow_blocking_init()


with such.A("system with a fast initial setup layer") as it:
    it.uses(Layer1)

    @it.should("not have obj initialized")
    def test():
        assert not it.obj

    with it.having("a second slow setup layer"):
        it.uses(Layer2)

        @it.should("have obj initialized")
        def test2():
            assert it.obj


it.createTests(globals())
