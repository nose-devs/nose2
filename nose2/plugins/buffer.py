"""
Buffer stdout and/or stderr during test execution, appending any
output to the error reports of failed tests.

This allows you to use print for debugging in tests without making
your test runs noisy.

This plugin implements :func:`startTest`, :func:`stopTest`,
:func:`setTestOutcome`, :func:`outcomeDetail`, :func:`beforeInteraction`
and :func:`afterInteraction` to manage capturing sys.stdout and/or
sys.stderr into buffers, attaching the buffered output to test error
report detail, and getting out of the way when other plugins want to
talk to the user.

"""

import sys
import traceback

from six import StringIO

from nose2 import events
from nose2.util import ln


__unittest = True


class _Buffer(object):

    def __init__(self, stream):
        self._stream = stream
        self._buffer = StringIO()

    def fileno(self):
        return self._stream.fileno()

    def __getattr__(self, attr):
        # this happens on unpickling
        if attr == '_buffer':
            raise AttributeError("No _buffer yet")
        return getattr(self._buffer, attr)

    def __le__(self, obj):
        return self._buffer.getvalue() == obj

    def __eq__(self, obj):
        return self._buffer.getvalue() == obj

    def __str__(self):
        return self._buffer.getvalue()

    def __repr__(self):
        return repr(self._buffer.getvalue())


class OutputBufferPlugin(events.Plugin):

    """Buffer output during test execution"""
    commandLineSwitch = ('B', 'output-buffer', 'Enable output buffer')
    configSection = 'output-buffer'

    def __init__(self):
        self.captureStdout = self.config.as_bool('stdout', default=True)
        self.captureStderr = self.config.as_bool('stderr', default=False)
        self.bufStdout = self.bufStderr = None
        self.realStdout = sys.__stdout__
        self.realStderr = sys.__stderr__
        self._disable = False

    def registerInSubprocess(self, event):
        event.pluginClasses.append(self.__class__)
        # turn off in this process: the subproc will run the tests
        self._disable = True

    def startSubprocess(self, event):
        self.realStdout = sys.__stdout__
        self.realStderr = sys.__stderr__

    def startTest(self, event):
        """Start buffering selected stream(s)"""
        self._buffer()

    def stopTest(self, event):
        """Stop buffering"""
        self._restore()

    def _get_stream_unicode_save(self, stream, buffer):
        buf = ''
        stream_buffer_exc_info = None
        try:
            buf = buffer.getvalue()
        except (UnicodeError, UnicodeDecodeError):
            # python2's StringIO.StringIO [1] class has this warning:
            #
            #     The StringIO object can accept either Unicode or 8-bit strings,
            #     but mixing the two may take some care. If both are used, 8-bit
            #     strings that cannot be interpreted as 7-bit ASCII (that use the
            #     8th bit) will cause a UnicodeError to be raised when getvalue()
            #     is called.
            #
            # This exception handler is a protection against crashes
            # caused by this exception (such as [2] in the original
            # nose application). Capturing the exception info allows us
            # to display it back to the user.
            #
            # [1] <https://github.com/python/cpython/blob/2.7/Lib/StringIO.py#L258>
            # [2] <https://github.com/nose-devs/nose/issues/816>
            stream_buffer_exc_info = sys.exc_info()
        extraDetail = []
        extraDetail.append(
            ln('>> begin captured %s <<' % stream))
        extraDetail.append(buf)
        extraDetail.append(ln('>> end captured %s <<' % stream))
        if stream_buffer_exc_info:
            extraDetail.append('OUTPUT ERROR: Could not get captured %s output.' % stream)
            extraDetail.append("The test might've printed both 'unicode' strings and non-ASCII 8-bit 'str' strings.")
            extraDetail.append(ln('>> begin captured %s exception traceback <<' % stream))
            extraDetail.append(''.join(traceback.format_exception(*stream_buffer_exc_info)))
            extraDetail.append(ln('>> end captured %s exception traceback <<' % stream))
        return "\n".join(extraDetail)

    def setTestOutcome(self, event):
        """Attach buffer(s) to event.metadata"""
        if self._disable:
            return
        if self.captureStdout and 'stdout' not in event.metadata:
            event.metadata['stdout'] = self._get_stream_unicode_save('stdout', self.bufStdout)
        if self.captureStderr and 'stderr' not in event.metadata:
            event.metadata['stderr'] = self._get_stream_unicode_save('stderr', self.bufStderr)

    def outcomeDetail(self, event):
        """Add buffered output to event.extraDetail"""
        for stream in ('stdout', 'stderr'):
            if stream in event.outcomeEvent.metadata:
                b = event.outcomeEvent.metadata[stream]
                if b:
                    event.extraDetail.append(b)

    def beforeInteraction(self, event):
        """Stop buffering so users can see stdout"""
        self._restore()

    def afterInteraction(self, event):
        """Start buffering again (does not clear buffers)"""
        self._buffer(fresh=False)

    def stopSubprocess(self, event):
        self._restore()

    def _restore(self):
        if self._disable:
            return
        if self.captureStdout:
            sys.stdout = self.realStdout
        if self.captureStderr:
            sys.stderr = self.realStderr

    def _buffer(self, fresh=True):
        if self._disable:
            return
        if self.captureStdout:
            if fresh or self.bufStdout is None:
                self.bufStdout = _Buffer(sys.stdout)
            sys.stdout = self.bufStdout
        if self.captureStderr:
            if fresh or self.bufStderr is None:
                self.bufStderr = _Buffer(sys.stderr)
            sys.stderr = self.bufStderr
