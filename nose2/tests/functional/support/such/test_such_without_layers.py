from nose2.tools import such

with such.A("system with complex setup") as it:

    @it.has_setup
    def setup():
        it.things = [1]

    @it.has_teardown
    def teardown():
        it.things = []

    @it.should("do something")
    def test():
        assert it.things
        it.assertEqual(len(it.things), 1)

    with it.having("an expensive fixture"):

        @it.has_setup  # noqa: F811
        def setup():  # noqa: F811
            it.things.append(2)

        @it.should("do more things")  # noqa: F811
        def test(case):  # noqa: F811
            case.assertEqual(it.things[-1], 2)


it.createTests(globals())
