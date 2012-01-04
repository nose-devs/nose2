from nose2 import events, loader, session
from nose2.tests._common import TestCase


class TestPluggableTestLoader(TestCase):
    def setUp(self):
        self.session = session.Session()
        self.loader = loader.PluggableTestLoader(self.session)

    def test_load_from_module_calls_hook(self):
        self.session.hooks.register('loadTestsFromModule', FakePlugin())
        evt = events.LoadFromModuleEvent(self.loader, 'some_module')
        self.session.hooks.loadTestsFromModule(evt)
        assert evt.fake, "FakePlugin was not called"


class FakePlugin(object):
    def loadTestsFromModule(self, event):
        event.fake = True

    def loadTestsFromNames(self, event):
        event.fake = True
