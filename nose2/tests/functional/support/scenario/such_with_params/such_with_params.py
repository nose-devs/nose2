from nose2.tools import such
from nose2.tools.params import params

with such.A('foo') as it:
    @it.should('do bar')
    @params(1,2,3)
    def test(case, bar):
        case.assert_(isinstance(bar, int))

    @it.should('do bar and extra')
    @params((1, 2), (3, 4) ,(5, 6))
    def testExtraArg(case, bar, foo):
        case.assert_(isinstance(bar, int))
        case.assert_(isinstance(foo, int))

it.createTests(globals())
