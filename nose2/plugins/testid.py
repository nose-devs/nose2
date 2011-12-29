import os
import pickle
import re

from nose2.events import Plugin


class TestId(Plugin):
    """TODO: document"""

    configSection = 'testid'
    commandLineSwitch = ('I', 'with-id', 'Add test ids to output')
    idpat = re.compile(r'(\d+)')

    def __init__(self):
        self.idfile = self.config.get('id-file', '.noseids')
        self.ids = {}
        self.tests = {}
        if not os.path.isabs(self.idfile):
            # FIXME expand-user?
            self.idfile = os.path.join(os.getcwd(), self.idfile)
        self.id = 0
        self._loaded = False

    def nextId(self):
        """Increment ID and return it.

        XXX: Make private?
        """
        self.id += 1
        return self.id

    def startTest(self, event):
        """Implement hook"""
        testid = event.test.id().split('\n')[0]
        if testid not in self.tests:
            id_ = self.nextId()
            self.ids[id_] = testid
            self.tests[testid] = id_
        else:
            id_ = self.tests[testid]
        event.message('#%s ' % id_, (2,))

    def loadTestsFromName(self, event):
        """Implement hook.

        If the name is a number, it might be an ID assigned by us. If we can
        find a test to which we have assigned that ID, event.name is changed to
        the test's real ID. In this way, tests can be referred to via sequential
        numbers.
        """
        testid = self._testNameFromId(event.name)
        if testid is not None:
            event.name = testid

    def loadTestsFromNames(self, event):
        """Implement hook."""
        for i, name in enumerate(event.names[:]):
            testid = self._testNameFromId(name)
            if testid is not None:
                event.names[i] = testid

    def stopTestRun(self, event):
        """Implement hook."""
        fh = open(self.idfile, 'wb')
        pickle.dump({'ids': self.ids, 'tests': self.tests}, fh)

    def loadIds(self):
        """Load previously pickled 'ids' and 'tests' attributes.

        XXX: Make private?
        """
        if self._loaded:
            return

        try:
            fh = open(self.idfile, 'rb')
        except EnvironmentError:
            self._loaded = True
            return
        try:
            data = pickle.load(fh)
        finally:
            fh.close()

        if 'ids' in data:
            self.ids = data['ids']
        if 'tests' in data:
            self.tests = data['tests']
        self.id = max(self.ids.keys())
        self._loaded = True


    def _testNameFromId(self, name):
        """Try to translate one of our IDs to real test ID."""
        m = self.idpat.match(name)
        if m is None:
            return None

        id_ = int(m.groups()[0])

        self.loadIds()
        # Translate to test's real ID
        try:
            return self.ids[id_]
        except KeyError:
            return None
