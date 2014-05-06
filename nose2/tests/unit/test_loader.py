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
        self.assertTrue(evt.fakeLoadFromModule,
                        "FakePlugin.loadTestsFromModule() was not called")

    def test_load_from_name_calls_hook(self):
        self.session.hooks.register('loadTestsFromName', FakePlugin())
        evt = events.LoadFromNameEvent(self.loader,
                                       'some_name',
                                       'some_module')
        self.session.hooks.loadTestsFromName(evt)
        self.assertTrue(evt.fakeLoadFromName,
                        "FakePlugin.fakeLoadFromName() was not called")

    def test_load_from_names_calls_hook(self):
        self.session.hooks.register('loadTestsFromNames', FakePlugin())
        evt = events.LoadFromNamesEvent(self.loader,
                                        ['name1', 'name2'],
                                        'some_module')
        self.session.hooks.loadTestsFromNames(evt)
        self.assertTrue(evt.fakeLoadFromNames,
                        "FakePlugin.fakeLoadFromNames() was not called")


class FakePlugin(object):

    def loadTestsFromModule(self, event):
        event.fakeLoadFromModule = True

    def loadTestsFromName(self, event):
        event.fakeLoadFromName = True

    def loadTestsFromNames(self, event):
        event.fakeLoadFromNames = True
