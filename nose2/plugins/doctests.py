import doctest
import os

from unittest2 import loader, Plugin


class DocTestLoader(Plugin):
    configSection = 'doctest'
    commandLineSwitch = (None, 'with-doctest',
                         'Look for doctests in all modules')

    def __init__(self):
        self.extensions = self.config.as_list('extensions', ['.txt', '.rst'])

    def handleFile(self, event):
        """Implement hook."""
        loader_ = event.loader
        path = event.path
        _root, ext = os.path.splitext(path)
        if ext in self.extensions:
            suite = doctest.DocFileTest(path, module_relative=False)
            event.extraTests.append(suite)
            return
        elif not loader.VALID_MODULE_NAME.match(os.path.basename(path)):
            return

        name = loader_._get_name_from_path(path)
        try:
            module = loader_._get_module_from_name(name)
        except:
            return
        if hasattr(module, '__test__') and not module.__test__:
            return
        try:
            suite = doctest.DocTestSuite(module)
        except ValueError:
            # doctest, very annoyingly, raises ValueError when
            # a module has no tests.
            return
        event.extraTests.append(suite)
