"""Common functionality for tests."""
class _FakeEventBase(object):
    """Baseclass for fake Events."""
    def __init__(self):
        self._fake_messages = []

    def message(self, msg, verbosity=(1, 2)):
        self._fake_messages.append((msg, verbosity))

class FakeStartTestEvent(_FakeEventBase):
    """Fake StartTestEvent."""
    def __init__(self, test):
        super(FakeStartTestEvent, self).__init__()
        self.test = test
        self.result = test.defaultTestResult()
        import time
        self.startTime = time.time()

class FakeLoadFromNameEvent(_FakeEventBase):
    """Fake LoadFromNameEvent."""
    def __init__(self, name):
        super(FakeLoadFromNameEvent, self).__init__()
        self.name = name

class FakeLoadFromNamesEvent(_FakeEventBase):
    """Fake LoadFromNamesEvent."""
    def __init__(self, names):
        super(FakeLoadFromNamesEvent, self).__init__()
        self.names = names
