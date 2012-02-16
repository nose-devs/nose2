"""
Start a :func:`pdb.post_mortem` on errors and failures.

This plugin implements :func:`testOutcome` and will drop into pdb
whenever it sees a test outcome that includes exc_info.

It fires :func:`beforeInteraction` before launching pdb and
:func:`afterInteraction` after. Other plugins may implement
:func:`beforeInteraction` to return False and set event.handled to
prevent this plugin from launching pdb.

"""
import logging
import pdb

from nose2 import events


__unittest = True
log = logging.getLogger(__name__)


class Debugger(events.Plugin):
    """Enter pdb on test error or failure

    .. attribute :: pdb

       For ease of mocking and using different pdb implementations, pdb
       is aliased as a class attribute.

    """
    configSection = 'debugger'
    commandLineSwitch = ('D', 'debugger', 'Enter pdb on test fail or error')
    # allow easy mocking and replacment of pdb
    pdb = pdb
    _mpmode = False

    def __init__(self):
        self.errorsOnly = self.config.as_bool('errors-only', default=False)

    def registerInSubprocess(self, event):
        self._mpmode = True
        log.warn("Disabled during multiprocess test run")

    def testOutcome(self, event):
        """Drop into pdb on unexpected errors or failures"""
        if self._mpmode:
            # can't interact with users during multiprocess runs
            log.warn("Skipping pdb for %s during multiprocess test run", event)
            return

        if not event.exc_info or event.expected:
            # skipped tests, unexpected successes, expected failures
            return

        value, tb = event.exc_info[1:]
        test = event.test
        if self.errorsOnly and isinstance(value, test.failureException):
            return
        event = events.UserInteractionEvent()
        result = self.session.hooks.beforeInteraction(event)
        if not result and event.handled:
            return
        try:
            self.pdb.post_mortem(tb)
        finally:
            self.session.hooks.afterInteraction(event)
