"""
Start a :func:`pdb.post_mortem` on errors and failures.

This plugin implements :func:`testOutcome` and will drop into pdb
whenever it sees a test outcome that includes exc_info.

It fires :func:`beforeInteraction` before launching pdb and
:func:`afterInteraction` after. Other plugins may implement
:func:`beforeInteraction` to return ``False`` and set ``event.handled`` to
prevent this plugin from launching pdb.

"""
import logging
import pdb
import sys

from nose2 import events


__unittest = True
log = logging.getLogger(__name__)


class Debugger(events.Plugin):

    """Enter pdb on test error or failure

    .. attribute :: pdb

       For ease of mocking and using different pdb implementations, the pdb
       module is aliased as a class attribute.  It can be set to another module
       that implements a class named `Pdb` using the `pdbmodule` command line
       argument, e.g. `--pdbmodule=IPython.core.debugger`.

    """
    configSection = 'debugger'
    commandLineSwitch = ('D', 'debugger', 'Enter pdb on test fail or error')
    # allow easy mocking and replacment of pdb
    pdb = pdb

    def __init__(self):
        self.errorsOnly = self.config.as_bool('errors-only', default=False)
        self.addArgument(
            self._set_pdbmodule, None, 'pdbmodule',
            'name of pdb module; should implement a class named "Pdb"')

    def _set_pdbmodule(self, pdbmodule):
        pdbmodule, = pdbmodule
        __import__(pdbmodule)
        self.pdb = sys.modules[pdbmodule]

    def testOutcome(self, event):
        """Drop into pdb on unexpected errors or failures"""
        if not event.exc_info or event.expected:
            # skipped tests, unexpected successes, expected failures
            return

        value, tb = event.exc_info[1:]
        test = event.test
        if self.errorsOnly and isinstance(value, test.failureException):
            return
        evt = events.UserInteractionEvent()
        result = self.session.hooks.beforeInteraction(evt)
        try:
            if not result and evt.handled:
                log.warning(
                    "Skipping pdb for %s, user interaction not allowed", event)
                return
            p = self.pdb.Pdb()
            p.reset()
            p.interaction(None, tb)
        finally:
            self.session.hooks.afterInteraction(evt)
