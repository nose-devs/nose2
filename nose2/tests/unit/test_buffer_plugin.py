import io
import sys

from nose2 import events, result, session, util
from nose2.plugins import buffer
from nose2.tests._common import TestCase


class TestBufferPlugin(TestCase):
    tags = ["unit"]

    def setUp(self):
        self.session = session.Session()
        self.result = result.PluggableTestResult(self.session)
        self.plugin = buffer.OutputBufferPlugin(session=self.session)
        self.plugin.register()

        class Test(TestCase):
            printed_nonascii_str = util.safe_decode("test 日本").encode("utf-8")
            printed_unicode = "hello"

            def test_out(self):
                print("hello")
                raise {}["oops"]

            def test_err(self):
                print("goodbye", file=sys.stderr)

            def test_mixed_unicode_and_nonascii_str(self):
                print(self.printed_nonascii_str)
                print(self.printed_unicode)
                print(self.printed_nonascii_str, file=sys.stderr)
                print(self.printed_unicode, file=sys.stderr)
                raise {}["oops"]

        self.case = Test

        class Watcher(events.Plugin):
            def __init__(self):
                self.events = []

            def testOutcome(self, event):
                self.events.append(event)

        self.watcher = Watcher(session=self.session)
        self.watcher.register()

    def test_captures_stdout(self):
        out = sys.stdout
        buf = io.StringIO()
        sys.stdout = buf
        try:
            test = self.case("test_out")
            test(self.result)
            assert "hello" not in buf.getvalue()
            assert "hello" in self.watcher.events[0].metadata["stdout"]
        finally:
            sys.stdout = out

    def test_captures_stderr_when_configured(self):
        self.plugin.captureStderr = True
        err = sys.stderr
        buf = io.StringIO()
        sys.stderr = buf
        try:
            test = self.case("test_err")
            test(self.result)
            assert "goodbye" not in buf.getvalue()
            assert "goodbye" in self.watcher.events[0].metadata["stderr"]
        finally:
            sys.stderr = err

    def test_does_not_crash_with_mixed_unicode_and_nonascii_str(self):
        self.plugin.captureStderr = True
        test = self.case("test_mixed_unicode_and_nonascii_str")
        test(self.result)
        evt = events.OutcomeDetailEvent(self.watcher.events[0])
        self.session.hooks.outcomeDetail(evt)
        extraDetail = "".join(evt.extraDetail)
        for string in [
            repr(self.case.printed_nonascii_str),
            self.case.printed_unicode,
        ]:
            assert string in extraDetail, "Output not found in error message"

    def test_decorates_outcome_detail(self):
        test = self.case("test_out")
        test(self.result)
        evt = events.OutcomeDetailEvent(self.watcher.events[0])
        self.session.hooks.outcomeDetail(evt)
        assert "hello" in "".join(evt.extraDetail)
