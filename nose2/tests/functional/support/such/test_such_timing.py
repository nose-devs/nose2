# Issue: https://github.com/nose-devs/nose2/issues/215
# From: https://gist.github.com/lukeorland/d4534a20241d7b5280b0
# Author: https://github.com/lukeorland
import time
from nose2.tools import such


def slow_blocking_init():
    time.sleep(2)
    return True


with such.A('system with a fast initial setup layer') as it:

    @it.has_setup
    def setup():
        it.obj = False

    @it.should('not have obj initialized')
    def test():
        assert not it.obj

    with it.having('a second slow setup layer'):

        @it.has_setup
        def setup():
            it.obj = slow_blocking_init()

        @it.should('have obj initialized')
        def test():
            assert it.obj

it.createTests(globals())
