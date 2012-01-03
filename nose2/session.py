import logging

import argparse
from six.moves import configparser

from nose2 import config, events, util


log = logging.getLogger(__name__)


class Session(object):
    """Configuration session.

    Encapsulates all configuration for a given test run.

    """
    def __init__(self):
        self.argparse = argparse.ArgumentParser(prog='nose2')
        self.config = configparser.ConfigParser()
        self.hooks = events.PluginInterface()
        self.plugins = []
        self.verbosity = 1

    def get(self, section):
        # FIXME cache these
        items = []
        if self.config.has_section(section):
            items = self.config.items(section)
        return config.Config(items)

    def loadConfigFiles(self, *filenames):
        self.config.read(filenames)

    def loadPlugins(self, modules=None):
        # plugins set directly
        if modules is None:
            modules = []
        # plugins mentioned in config file(s)
        cfg = self.get('unittest')
        more_plugins = cfg.as_list('plugins', [])
        exclude = set(cfg.as_list('excluded-plugins', []))
        all_  = set(modules + more_plugins) - exclude
        log.debug("Loading plugin modules: %s", all_)
        for module in all_:
            self.loadPluginsFromModule(util.module_from_name(module))
        self.hooks.loadedPlugins(events.PluginsLoadedEvent(self.plugins))

    def loadPluginsFromModule(self, module):
        avail = []
        for entry in dir(module):
            try:
                item = getattr(module, entry)
            except AttributeError:
                pass
            try:
                if issubclass(item, events.Plugin):
                    avail.append(item)
            except TypeError:
                pass
        for cls in avail:
            log.debug("Plugin is available: %s", cls)
            self.plugins.append(cls(session=self))

    def registerPlugin(self, plugin):
        log.debug("Register active plugin %s", plugin)
        if plugin not in self.plugins:
            self.plugins.append(plugin)
        for method in self.hooks.methods:
            if hasattr(plugin, method):
                log.debug("Register method %s for plugin %s", method, plugin)
                self.hooks.register(method, plugin)

    # convenience properties
    @property
    def testFilePattern(self):
        return self.get('unittest').as_str('test-file-pattern', 'test*.py')

    @property
    def testMethodPrefix(self):
        return self.get('unittest').as_str('test-method-prefix', 'test')
