import inspect

from unittest2 import Plugin
from unittest2.events import hooks
from unittest2.util import getObjectFromName


class LoaderCompat(Plugin):
    configSection = 'compat'

    def pluginsLoaded(self, event):
        # ensure that my hook calls come first
        hook = hooks.loadTestsFromModule
        hook -= self.loadTestsFromModule
        hook += self.loadTestsFromModule

    #def loadTestsFromName(self, event):
    #    parent, obj = getObjectFromName(event.name, event.module)
    #    self._update(obj)

    def loadTestsFromModule(self, event):
        module = event.module
        # shim to make nose-style implicit generators
        # and test function fixtures work with moduleloading plugin
        for attr in dir(module):
            item = getattr(module, attr, None)
            self._update(item)

    def _update(self, obj):
        if inspect.isfunction(obj):
            if hasattr(obj, 'setup'):
                obj.setUp = obj.setup
            elif hasattr(obj, 'setUpFunc'):
                obj.setUp = obj.setUpFunc
            if hasattr(obj, 'teardown'):
                obj.tearDown = obj.teardown
            elif hasattr(obj, 'tearDownFunc'):
                obj.tearDown = obj.tearDownFunc
            if inspect.isgeneratorfunction(obj):
                obj.testGenerator = True
