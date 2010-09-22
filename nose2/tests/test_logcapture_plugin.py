import logging
import re
import unittest2

from . import FunctionalTestCase
from ..plugins.logcapture import LogCapture


log = logging.getLogger(__name__)


class LogCaptureFunctionalTest(FunctionalTestCase):
    def test_layout2(self):
        match = re.compile('>> begin captured logging <<')
        self.assertTestRunOutputMatches(
            self.runIn('layout2'),
            stderr=match)


class LogCaptureUnitTest(unittest2.TestCase):

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
