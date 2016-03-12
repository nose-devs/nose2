from nose2.tools import such
import logging
from .common import UniqueResource, NormalTest, NormalTestTwo
log = logging.getLogger(__name__)


with such.A('system with setup') as it:

    @it.has_setup
    def setup():
        log.info("Called setup in such test")
        it.unique_resource = UniqueResource()
        it.unique_resource.lock()

    @it.has_teardown
    def teardown():
        log.info("Called teardown in such test")
        it.unique_resource.unlock()

    @it.should('do something')
    def test(case):
        it.assertTrue(it.unique_resource.used)

it.createTests(globals())
