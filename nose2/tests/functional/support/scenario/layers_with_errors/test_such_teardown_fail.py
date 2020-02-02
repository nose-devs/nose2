from nose2.tools import such

with such.A("test scenario with errors") as it:

    @it.has_teardown
    def teardown_fail():
        raise RuntimeError("Bad Error in such tearDown!")

    @it.should("check that value == 1")
    def test_passes(case):
        pass


it.createTests(globals())
