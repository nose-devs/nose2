try:
    import hotshot
    from hotshot import stats
except ImportError:
    hotshot, stats = None, None
import os
import tempfile

from nose2.events import Plugin


class Profiler(Plugin):
    """TODO: document"""

    configSection = 'profiler'
    commandLineSwitch = ('P', 'profile', 'Run tests under profiler')

    def __init__(self):
        self.pfile = self.config.as_str('filename', '')
        self.sort = self.config.as_str('sort', 'cumulative')
        self.restrict = self.config.as_list('restrict', [])
        self.clean = False
        self.fileno = None

    def startTestRun(self, event):
        if not hotshot:
            return
        self.createPfile()
        self.prof = hotshot.Profile(self.pfile)
        event.executeTests = self.prof.runcall

    def runProf(self, result):
        self.prof.runcall(self.suite, result)

    def beforeSummaryReport(self, event):
        if not hotshot:
            return
        # write prof output to stream
        class Stream:
            def write(self, *msg):
                for m in msg:
                    event.message(unicode(m), (0, 1, 2))
                    event.message(u' ', (0, 1, 2))
        stream = Stream()
        self.prof.close()
        prof_stats = stats.load(self.pfile)
        prof_stats.sort_stats(self.sort)
        result = event.result
        if hasattr(result, 'separator1'):
            event.message(result.separator1, (0, 1, 2))
        event.message("\nProfiling results\n", (0, 1, 2))
        if hasattr(result, 'separator2'):
            event.message(result.separator2, (0, 1, 2))
        compat_25 = hasattr(prof_stats, 'stream')
        if compat_25:
            tmp = prof_stats.stream
            prof_stats.stream = stream
        else:
            tmp = sys.stdout
            sys.stdout = stream
        try:
            if self.restrict:
                prof_stats.print_stats(*self.restrict)
            else:
                prof_stats.print_stats()
        finally:
            if compat_25:
                prof_stats.stream = tmp
            else:
                sys.stdout = tmp
        self.prof.close()
        event.message("\n", (0, 1, 2))

        if self.clean:
            if self.fileno:
                try:
                    os.close(self.fileno)
                except OSError:
                    pass
            try:
                os.unlink(self.pfile)
            except OSError:
                pass

    def createPfile(self):
        if not self.pfile:
            self.fileno, self.pfile = tempfile.mkstemp()
            self.clean = True
