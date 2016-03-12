import logging
log = logging.getLogger(__name__)

from nose2.tools import such

with such.A('foo') as it:
    it.upper_run = 0
    it.lower_run = 0
    
    @it.has_setup
    def upper_test_setup(case):
        log.error('foo::setUp')
        it.upper_run += 1
 
    with it.having('some bar'):
        @it.has_setup
        def lower_test_setup(case):
            log.error('foo some bar::setUp')
            it.lower_run += 1
 
        @it.should("run all setups")
        def test_run_all_setups(case):
            case.assertEquals(it.upper_run, 1)
            case.assertEquals(it.lower_run, 1)

        @it.should("run all setups just once")
        def test_run_all_setups_just_once(case):
            case.assertEquals(it.upper_run, 1)
            case.assertEquals(it.lower_run, 1)

it.createTests(globals())
