from nose2 import session
from nose2.plugins import prof
from nose2.events import StartTestRunEvent
from nose2.tests._common import Stub, TestCase


class TestProfPlugin(TestCase):
    tags = ['unit']

    def setUp(self):
        self.plugin = prof.Profiler(session=session.Session())
        # stub out and save the cProfile and pstats modules
        self.cProfile = prof.cProfile
        self.pstats = prof.pstats
        prof.cProfile = Stub()
        prof.pstats = Stub()

    def tearDown(self):
        prof.cProfile = self.cProfile
        prof.pstats = self.pstats

    def test_startTestRun_sets_executeTests(self):
        _prof = Stub()
        _prof.runcall = object()
        prof.cProfile.Profile = lambda: _prof
        event = StartTestRunEvent(runner=None, suite=None, result=None,
                                  startTime=None, executeTests=None)
        self.plugin.startTestRun(event)
        assert event.executeTests is _prof.runcall, \
            "executeTests was not replaced"
