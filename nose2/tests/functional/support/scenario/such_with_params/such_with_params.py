from nose2.tools import such
from nose2.tools.params import params

with such.A("foo") as it:

    @it.should("do bar")
    @params(1, 2, 3)
    def test(case, bar):
        case.assertTrue(isinstance(bar, int))

    @it.should("do bar and extra")
    @params((1, 2), (3, 4), (5, 6))
    def testExtraArg(case, bar, foo):
        case.assertTrue(isinstance(bar, int))
        case.assertTrue(isinstance(foo, int))


it.createTests(globals())
