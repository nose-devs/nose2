import os
import pickle
import re
from unittest2.events import Plugin


class TestId(Plugin):
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
        self.id += 1
        return self.id

    def startTest(self, event):
        testid = event.test.id()
        if testid not in self.tests:
            id_ = self.nextId()
            self.ids[id_] = testid
            self.tests[testid] = id_
        else:
            id_ = self.tests[testid]
        event.message('#%s ' % id_, (2,))

    def loadTestsFromName(self, event):
        self.loadIds()
        id_ = self.argToId(event.name)
        if id_ and id_ in self.ids:
            event.name = self.ids[id_]

    def loadTestsFromNames(self, event):
        self.loadIds()
        new_names = []
        for name in event.names:
            if self.argToId(name) in self.ids:
                new_names.append(self.ids[name])
            else:
                new_names.append(name)
        event.names[:] = new_names

    def stopTestRun(self, event):
        fh = open(self.idfile, 'w')
        pickle.dump({'ids': self.ids, 'tests': self.tests}, fh)

    def argToId(self, name):
        m = self.idpat.match(name)
        if m:
            return int(m.groups()[0])

    def loadIds(self):
        if self._loaded:
            return
        fh = open(self.idfile, 'r')
        data = pickle.load(fh)
        if 'ids' in data:
            self.ids = data['ids']
        if 'tests' in data:
            self.tests = data['tests']
        self.id = max(self.ids.keys())
        self._loaded = True
