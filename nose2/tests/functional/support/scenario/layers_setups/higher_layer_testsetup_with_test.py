import logging

from nose2.tools import such

log = logging.getLogger(__name__)


with such.A("foo") as it:
    it.upper_run = 0
    it.lower_run = 0

    @it.has_test_setup
    def upper_test_setup(case):
        log.error("foo::setUp")
        it.upper_run += 1

    @it.should("run upper setups")
    def test_run_upper_setups(case):
        case.assertEqual(it.upper_run, 1)
        case.assertEqual(it.lower_run, 0)

    with it.having("some bar"):

        @it.has_test_setup
        def lower_test_setup(case):
            log.error("foo some bar::setUp")
            it.lower_run += 1

        @it.should("run all setups")
        def test_run_all_setups(case):
            case.assertEqual(it.upper_run, 2)
            case.assertEqual(it.lower_run, 1)

        @it.should("run all setups again")
        def test_run_all_setups_again(case):
            case.assertEqual(it.upper_run, 3)
            case.assertEqual(it.lower_run, 2)


it.createTests(globals())
