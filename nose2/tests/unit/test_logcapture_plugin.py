import logging

from nose2.tests._common import TestCase
from nose2.plugins.logcapture import LogCapture


log = logging.getLogger(__name__)


class LogCaptureUnitTest(TestCase):
    tags = ['unit']

    def setUp(self):
        self.plugin = LogCapture()

    def event(self, error=True, failed=False):
        e = Event()
        e.error = True
        e.failed = False
        e.traceback = ''
        e.metadata = {}
        return e

    def test_buffer_cleared_after_each_test(self):
        self.plugin.startTestRun(None)
        self.plugin.startTest(None)
        log.debug("hello")
        assert self.plugin.handler.buffer
        self.plugin.stopTest(self.event())
        assert not self.plugin.handler.buffer

    def test_buffered_logs_attached_to_event(self):
        self.plugin.startTestRun(None)
        self.plugin.startTest(None)
        log.debug("hello")
        assert self.plugin.handler.buffer
        e = self.event()
        self.plugin.stopTest(e)
        assert 'logs' in e.metadata, "No log in %s" % e.metadata
        assert e.traceback


class Event:
    pass
