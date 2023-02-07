#!/usr/bin/env python

from nose2.tools import such

with such.A("system") as it:
    with it.having("something"):

        @it.should("do stuff")
        def test_should_do_stuff(case):
            pass

    it.createTests(globals())

with such.A("another system") as it:
    with it.having("something"):

        @it.should("do stuff")  # noqa: F811
        def test_should_do_stuff(case):  # noqa: F811
            pass

    it.createTests(globals())
