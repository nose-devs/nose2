# Issue: https://github.com/nose-devs/nose2/issues/215
# From: https://gist.github.com/lukeorland/d4534a20241d7b5280b0
# Author: https://github.com/lukeorland
import unittest
import time
from nose2.tools import such


def slow_blocking_init():
    time.sleep(2)
    return True


class Layer1(unittest.TestCase):
    @classmethod
    def setUp(cls):
        it.obj = False


class Layer2(unittest.TestCase):
    @classmethod
    def setUp(cls):
        it.obj = slow_blocking_init()


with such.A('system with a fast initial setup layer') as it:

    it.uses(Layer1)

    @it.should('not have obj initialized')
    def test():
        assert not it.obj

    with it.having('a second slow setup layer'):

        it.uses(Layer2)

        @it.should('have obj initialized')
        def test():
            assert it.obj


it.createTests(globals())
