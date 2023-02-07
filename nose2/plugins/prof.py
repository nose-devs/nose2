"""
Profile test execution using cProfile.

This plugin implements :func:`startTestRun` and replaces
``event.executeTests`` with :meth:`cProfile.Profile.runcall`. It
implements :func:`beforeSummaryReport` to output profiling information
before the final test summary time. Config file options ``filename``,
``sort`` and ``restrict`` can be used to change where profiling
information is saved and how it is presented.

Load this plugin by running nose2 with the
`--plugin=nose2.plugins.prof` option and activate it
with the `--profile` option,or put the corresponding
entries (`plugin` and `always_on`) in the respective
sections of the configuration file.

"""
import cProfile
import logging
import pstats

from nose2 import events, util

log = logging.getLogger(__name__)
__unittest = True


class Profiler(events.Plugin):

    """Profile the test run"""

    configSection = "profiler"
    commandLineSwitch = ("P", "profile", "Run tests under profiler")

    def __init__(self):
        self.pfile = self.config.as_str("filename", "")
        self.sort = self.config.as_str("sort", "cumulative")
        self.restrict = self.config.as_list("restrict", [])
        self.fileno = None

    def startTestRun(self, event):
        """Set up the profiler"""
        self.prof = cProfile.Profile()
        event.executeTests = self.prof.runcall

    def beforeSummaryReport(self, event):
        """Output profiling results"""

        # write prof output to stream
        class Stream:
            def write(self, *msg):
                for m in msg:
                    event.stream.write(m)
                    event.stream.write(" ")
                event.stream.flush()

        stream = Stream()
        prof_stats = pstats.Stats(self.prof, stream=stream)
        prof_stats.sort_stats(self.sort)
        event.stream.writeln(util.ln("Profiling results"))
        if self.restrict:
            prof_stats.print_stats(*self.restrict)
        else:
            prof_stats.print_stats()

        if self.pfile:
            prof_stats.dump_stats(self.pfile)

        self.prof.disable()
        event.stream.writeln("")
