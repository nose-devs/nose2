from nose2.tools import such

with such.A('thing that tests stuff') as it:

    @it.has_setup
    def setup():
        it.things = [1]

    @it.has_teardown
    def teardown():
        it.things = []

    @it.should('do something')
    def test():
        assert it.things

    with it.having('some thing that is whatever'):
        @it.has_setup
        def setup():
            it.things.append(2)

        @it.should('do more things')
        def test(case):
            case.assertEqual(it.things[-1], 2)

        with it.having('another precondtion'):
            @it.has_setup
            def setup():
                it.things.append(3)

            @it.has_teardown
            def teardown():
                it.things.pop()

            @it.should('do that not this')
            def test(case):
                it.things.append(4)
                case.has_teardown(lambda: it.things.pop())
                case.assertEqual(it.things[-1], 4, it.things)

            @it.should('do this not that')
            def test(case):
                case.assertEqual(it.things[-1], 3, it.things)

        with it.having('a different precondition'):
            @it.has_setup
            def setup():
                it.things.append(99)

            @it.has_teardown
            def teardown():
                it.things.pop()

            @it.has_test_setup
            def test_setup():
                it.is_funny = True

            @it.has_test_teardown
            def test_teardown():
                delattr(it, 'is_funny')

            @it.should('do something else')
            def test():
                assert it.things[-1] == 99
                assert it.is_funny

            @it.should('also do something else again')
            def test():
                assert it.is_funny

            @it.should('go get me a sandwich')
            def test():
                assert it.is_funny
