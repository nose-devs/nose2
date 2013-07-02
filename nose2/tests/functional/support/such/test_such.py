import unittest

from nose2.tools import such


class SomeLayer(object):

    @classmethod
    def setUp(cls):
        it.somelayer = True

    @classmethod
    def tearDown(cls):
        del it.somelayer

#
# Such tests start with a declaration about the system under test
# and will typically bind the test declaration to a variable with
# a name that makes nice sentences, like 'this' or 'it'.
#
with such.A('system with complex setup') as it:

    #
    # Each layer of tests can define setup and teardown methods.
    # setup and teardown methods defined here run around the entire
    # group of tests, not each individual test.
    #
    @it.has_setup
    def setup():
        it.things = [1]

    @it.has_teardown
    def teardown():
        it.things = []

    #
    # The 'should' decorator is used to mark tests.
    #
    @it.should('do something')
    def test():
        assert it.things
        #
        # Tests can use all of the normal unittest TestCase assert
        # methods by calling them on the test declaration.
        #
        it.assertEqual(len(it.things), 1)

    #
    # The 'having' context manager is used to introduce a new layer,
    # one that depends on the layer(s) above it. Tests in this
    # new layer inherit all of the fixtures of the layer above.
    #
    with it.having('an expensive fixture'):
        @it.has_setup
        def setup():
            it.things.append(2)

        #
        # Tests that take an argument will be passed the
        # unittest.TestCase instance that is generated to wrap
        # them. Tests can call any and all TestCase methods on this
        # instance.
        #
        @it.should('do more things')
        def test(case):
            case.assertEqual(it.things[-1], 2)

        #
        # Layers can be nested to any depth.
        #
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
                #
                # Tests can add their own cleanup functions.
                #
                case.addCleanup(it.things.pop)
                case.assertEqual(it.things[-1], 4, it.things)

            @it.should('do this not that')
            def test(case):
                case.assertEqual(it.things[-1], 3, it.things[:])

        #
        # A layer may have any number of sub-layers.
        #
        with it.having('a different precondition'):

            #
            # A layer defined with ``having`` can make use of
            # layers defined elsewhere. An external layer
            # pulled in with ``it.uses`` becomes a parent
            # of the current layer (though it doesn't actually
            # get injected into the layer's MRO).
            #
            it.uses(SomeLayer)

            @it.has_setup
            def setup():
                it.things.append(99)

            @it.has_teardown
            def teardown():
                it.things.pop()

            #
            # Layers can define setup and teardown methods that wrap
            # each test case, as well, corresponding to TestCase.setUp
            # and TestCase.tearDown.
            #
            @it.has_test_setup
            def test_setup(case):
                it.is_funny = True
                case.is_funny = True

            @it.has_test_teardown
            def test_teardown(case):
                delattr(it, 'is_funny')
                delattr(case, 'is_funny')

            @it.should('do something else')
            def test(case):
                assert it.things[-1] == 99
                assert it.is_funny
                assert case.is_funny

            @it.should('have another test')
            def test(case):
                assert it.is_funny
                assert case.is_funny

            @it.should('have access to an external fixture')
            def test(case):
                assert it.somelayer

            with it.having('a case inside the external fixture'):
                @it.should('still have access to that fixture')
                def test(case):
                    assert it.somelayer

#
# To convert the layer definitions into test cases, you have to call
# `createTests` and pass in the module globals, so that the test cases
# and layer objects can be inserted into the module.
#
it.createTests(globals())


#
# Such tests and normal tests can coexist in the same modules.
#
class NormalTest(unittest.TestCase):

    def test(self):
        pass
