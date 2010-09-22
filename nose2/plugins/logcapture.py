import logging
from logging.handlers import BufferingHandler
from StringIO import StringIO
import threading
from unittest2.events import Plugin, addOption

from nose2.util import ln


log = logging.getLogger(__name__)


class LogCapture(Plugin):
    configSection = 'logging'
    commandLineSwitch = (None, 'log-capture', 'Enable log capture')
    logformat = '%(name)s: %(levelname)s: %(message)s'
    logdatefmt = None
    clear = False
    filters = ['-nose']

    def __init__(self):
        self.logformat = self.config.as_str('format', self.logformat)
        self.logdatefmt = self.config.as_str('date-format', self.logdatefmt)
        self.filters = self.config.as_list('filter', self.filters)
        self.clear = self.config.as_bool('clear-handlers', self.clear)

    def setupLoghandler(self):
        # setup our handler with root logger
        root_logger = logging.getLogger()
        if self.clear:
            if hasattr(root_logger, "handlers"):
                for handler in root_logger.handlers:
                    root_logger.removeHandler(handler)
            for logger in logging.Logger.manager.loggerDict.values():
                if hasattr(logger, "handlers"):
                    for handler in logger.handlers:
                        logger.removeHandler(handler)
        # make sure there isn't one already
        # you can't simply use "if self.handler not in root_logger.handlers"
        # since at least in unit tests this doesn't work --
        # LogCapture() is instantiated for each test case while root_logger
        # is module global
        # so we always add new MyMemoryHandler instance
        for handler in root_logger.handlers[:]:
            if isinstance(handler, MyMemoryHandler):
                root_logger.handlers.remove(handler)
        root_logger.addHandler(self.handler)
        # to make sure everything gets captured
        root_logger.setLevel(logging.NOTSET)

    def addCapturedLogs(self, event):
        format = self.handler.format
        records = [format(r) for r in self.handler.buffer]
        event.metadata['logs'] = records
        # FIXME when there's a better way, do that instead
        records = [ln('>> begin captured logging <<')] + records + [
            ln('>> end captured logging <<')]
        records = u'\n'.join(records)
        event.traceback = "%s\n%s" % (
            event.traceback, records.encode('utf-8'))

    def startTestRun(self, event):
        self.handler = MyMemoryHandler(1000, self.logformat, self.logdatefmt,
                                       self.filters)
        self.setupLoghandler()

    def startTest(self, event):
        self.setupLoghandler()

    def stopTest(self, event):
        if event.error or event.failed:
            self.addCapturedLogs(event)
        self.handler.truncate()


class FilterSet(object):
    def __init__(self, filter_components):
        self.inclusive, self.exclusive = self._partition(filter_components)

    @staticmethod
    def _partition(components):
        inclusive, exclusive = [], []
        for component in components:
            if component.startswith('-'):
                exclusive.append(component[1:])
            else:
                inclusive.append(component)
        return inclusive, exclusive

    def allow(self, record):
        """returns whether this record should be printed"""
        if not self:
            # nothing to filter
            return True
        return self._allow(record) and not self._deny(record)

    @staticmethod
    def _any_match(matchers, record):
        """return the bool of whether `record` starts with
        any item in `matchers`"""
        def record_matches_key(key):
            return record == key or record.startswith(key + '.')
        return any(map(record_matches_key, matchers))

    def _allow(self, record):
        if not self.inclusive:
            return True
        return self._any_match(self.inclusive, record)

    def _deny(self, record):
        if not self.exclusive:
            return False
        return self._any_match(self.exclusive, record)


class MyMemoryHandler(BufferingHandler):
    def __init__(self, capacity, logformat, logdatefmt, filters):
        BufferingHandler.__init__(self, capacity)
        fmt = logging.Formatter(logformat, logdatefmt)
        self.setFormatter(fmt)
        self.filterset = FilterSet(filters)

    def flush(self):
        pass # do nothing

    def truncate(self):
        self.buffer = []

    def filter(self, record):
        return self.filterset.allow(record.name)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['lock']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.lock = threading.RLock()
