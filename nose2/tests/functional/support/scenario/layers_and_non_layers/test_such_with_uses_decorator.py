import logging

from nose2.tools import such

from .common import NormalTest, NormalTestTwo, UniqueResource  # noqa: F401

log = logging.getLogger(__name__)


class Layer1:
    description = "Layer1"

    @classmethod
    def setUp(cls):
        log.info("Called setup in layer 1")
        it.unique_resource = UniqueResource()
        it.unique_resource.lock()

    @classmethod
    def tearDown(cls):
        log.info("Called teardown in layer 2")
        it.unique_resource.unlock()


class Layer2:
    description = "Layer2"

    @classmethod
    def setUp(cls):
        log.info("Called setup in layer 2")

    @classmethod
    def tearDown(cls):
        log.info("Called teardown in layer 2")


with such.A("system with setup") as it:
    it.uses(Layer1)

    @it.should("do something")
    def test(case):
        it.assertTrue(it.unique_resource.used)

    with it.having("another setup"):
        it.uses(Layer2)

        @it.should("do something else")  # noqa: F811
        def test(case):  # noqa: F811
            it.assertTrue(it.unique_resource.used)


it.createTests(globals())
