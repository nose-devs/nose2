from nose2.tests._common import FunctionalTestCase, support_file
from nose2 import events, loader, session
from nose2.plugins.loader.discovery import DiscoveryLoader


class Watcher(events.Plugin):
    def __init__(self):
        self.called = []

    def loadTestsFromModule(self, event):
        self.called.append(event)


class DiscoveryFunctionalTest(FunctionalTestCase):
    def setUp(self):
        self.session = session.Session()
        self.plug = DiscoveryLoader(session=self.session)
        self.loader = loader.PluggableTestLoader(self.session)

    def test_createTests_hook(self):
        self.plug.start_dir = support_file('scenario/tests_in_package')
        watcher = Watcher(session=self.session)
        watcher.register()
        event = events.CreateTestsEvent(self.loader, None, None)
        result = self.session.hooks.createTests(event)
        assert isinstance(result, self.loader.suiteClass)
        assert watcher.called

