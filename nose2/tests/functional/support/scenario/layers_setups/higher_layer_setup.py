import logging

from nose2.tools import such

log = logging.getLogger(__name__)


with such.A("foo") as it:
    it.upper_run = 0
    it.lower_run = 0

    @it.has_setup
    def upper_test_setup(case):
        log.error("foo::setUp")
        it.upper_run += 1

    with it.having("some bar"):

        @it.has_setup
        def lower_test_setup(case):
            log.error("foo some bar::setUp")
            it.lower_run += 1

        @it.should("run all setups")
        def test_run_all_setups(case):
            case.assertEqual(it.upper_run, 1)
            case.assertEqual(it.lower_run, 1)

        @it.should("run all setups just once")
        def test_run_all_setups_just_once(case):
            case.assertEqual(it.upper_run, 1)
            case.assertEqual(it.lower_run, 1)


it.createTests(globals())
