import inspect

from unittest2 import Plugin
from unittest2.events import hooks


class LoaderCompat(Plugin):
    configSection = 'compat'

    def pluginsLoaded(self, event):
        # ensure that my hook call comes first
        hook = hooks.loadTestsFromModule
        hook -= self.loadTestsFromModule
        hook += self.loadTestsFromModule

    def loadTestsFromModule(self, event):
        module = event.module
        # shim to make nose-style implicit generators
        # and test function fixtures work with moduleloading plugin
        for attr in dir(module):
            item = getattr(module, attr, None)
            if inspect.isfunction(item):
                if hasattr(item, 'setup'):
                    item.setUp = item.setup
                elif hasattr(item, 'setUpFunc'):
                    item.setUp = item.setUpFunc
                if hasattr(item, 'teardown'):
                    item.tearDown = item.teardown
                elif hasattr(item, 'tearDownFunc'):
                    item.tearDown = item.tearDownFunc
                if inspect.isgeneratorfunction(item):
                    item.testGenerator = True
