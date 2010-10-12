import unittest2

from ..plugins import prof
from ._common import Stub, FakeStartTestRunEvent


class TestProfPlugin(unittest2.TestCase):
    tags = ['unit']

    def setUp(self):
        self.plugin = prof.Profiler()
        self.hotshot = prof.hotshot
        self.stats = prof.stats
        prof.hotshot = Stub()
        prof.stats = Stub()

    def tearDown(self):
        prof.hotshot = self.hotshot
        prof.stats = self.stats

    def test_start_test_run_sets_executeTests(self):
        _prof = Stub()
        _prof.runcall = object()
        prof.hotshot.Profile = lambda filename: _prof
        event = FakeStartTestRunEvent()
        self.plugin.startTestRun(event)
        assert event.executeTests is _prof.runcall, \
            "executeTests was not replaced"

