from nose2.tools import such

with such.A("test scenario with errors") as it:

    @it.has_setup
    def set_value():
        it.value = 1

    @it.should("check that value == 1")
    def test_passes(case):
        case.assertEqual(it.value, 1)

    @it.should("check that value == 2 and fail")
    def test_fails(case):
        case.assertEqual(it.value, 2)

    @it.should("check for an attribute that does not exist and raise an error")
    def test_err(case):
        case.assertEqual(it.mulch, "pine")


it.createTests(globals())
