import logging
import os

import argparse
from six.moves import configparser

from nose2 import config, events, util


log = logging.getLogger(__name__)
__unittest = True


class Session(object):

    """Configuration session.

    Encapsulates all configuration for a given test run.

    .. attribute :: argparse

       An instance of :class:`argparse.ArgumentParser`. Plugins can
       use this directly to add arguments and argument groups, but
       *must* do so in their ``__init__`` methods.

    .. attribute :: pluginargs

       The argparse argument group in which plugins (by default) place
       their command-line arguments. Plugins can use this directly to
       add arguments, but *must* do so in their ``__init__`` methods.

    .. attribute :: hooks

       The :class:`nose2.events.PluginInterface` instance contains
       all available plugin methods and hooks.

    .. attribute :: plugins

       The list of loaded -- but not necessarily *active* -- plugins.

    .. attribute :: verbosity

       Current verbosity level. Default: 1.

    .. attribute :: startDir

       Start directory of test run. Test discovery starts
       here. Default: current working directory.

    .. attribute :: topLevelDir

       Top-level directory of test run. This directory is added to
       sys.path. Default: starting directory.

    .. attribute :: libDirs

       Names of code directories, relative to starting
       directory. Default: ['lib', 'src']. These directories are added
       to sys.path and discovery if the exist.

    .. attribute :: testFilePattern

       Pattern used to discover test module files. Default: test*.py

    .. attribute :: testMethodPrefix

       Prefix used to discover test methods and functions: Default: 'test'.

    .. attribute :: unittest

       The config section for nose2 itself.

    """
    configClass = config.Config

    def __init__(self):
        self.argparse = argparse.ArgumentParser(prog='nose2', add_help=False)
        self.pluginargs = self.argparse.add_argument_group(
            'plugin arguments',
            'Command-line arguments added by plugins:')
        # py2/py3 compatible load of SafeConfigParser/ConfigParser
        self.config = getattr(configparser, "SafeConfigParser",
                              configparser.ConfigParser)()
        self.hooks = events.PluginInterface()
        self.plugins = []
        # this will be reset later, whenever handleCfgArgs happens, but it
        # starts at 1 so that it always has a non-negative integer value
        self.verbosity = 1
        self.startDir = None
        self.topLevelDir = None
        self.testResult = None
        self.testLoader = None
        self.logLevel = logging.WARN
        self.configCache = dict()

    def get(self, section):
        """Get a config section.

        :param section: The section name to retreive.
        :returns: instance of self.configClass.

        """
        # If section exists in cache, return cached version
        if section in self.configCache:
            return self.configCache[section]

        # If section doesn't exist in cache, parse config file
        # (and cache result)
        items = []
        if self.config.has_section(section):
            items = self.config.items(section)
        self.configCache[section] = self.configClass(items)
        return self.configCache[section]

    def loadConfigFiles(self, *filenames):
        """Load config files.

        :param filenames: Names of config files to load.

        Loads all names files that exist into ``self.config``.

        """
        self.config.read(filenames)

    def loadPlugins(self, modules=None, exclude=None):
        """Load plugins.

        :param modules: List of module names from which to load plugins.

        """
        # plugins set directly
        if modules is None:
            modules = []
        if exclude is None:
            exclude = []
        # plugins mentioned in config file(s)
        cfg = self.unittest
        more_plugins = cfg.as_list('plugins', [])
        cfg_exclude = cfg.as_list('exclude-plugins', [])
        exclude.extend(cfg_exclude)
        exclude = set(exclude)
        all_ = (set(modules) | set(more_plugins)) - exclude
        log.debug("Loading plugin modules: %s", all_)
        for module in sorted(all_):
            self.loadPluginsFromModule(util.module_from_name(module))
        self.hooks.pluginsLoaded(events.PluginsLoadedEvent(self.plugins))

    def loadPluginsFromModule(self, module):
        """Load plugins from a module.

        :param module: A python module containing zero or more plugin
                       classes.

        """
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
            plugin = cls(session=self)
            self.plugins.append(plugin)
            for method in self.hooks.preRegistrationMethods:
                if hasattr(plugin, method):
                    self.hooks.register(method, plugin)

    def registerPlugin(self, plugin):
        """Register a plugin.

        :param plugin: A `nose2.events.Plugin` instance.

        Register the plugin with all methods it implements.

        """
        log.debug("Register active plugin %s", plugin)
        if plugin not in self.plugins:
            self.plugins.append(plugin)
        for method in self.hooks.methods:
            if hasattr(plugin, method):
                log.debug("Register method %s for plugin %s", method, plugin)
                self.hooks.register(method, plugin)

    def setVerbosity(self, args_verbosity, args_verbose, args_quiet):
        """
        Determine verbosity from various (possibly conflicting) sources of info

        :param args_verbosity: The --verbosity argument value
        :param args_verbose: count of -v options
        :param args_quiet: count of -q options

        start with config, override with any given --verbosity, then adjust
        up/down with -vvv -qq, etc
        """
        self.verbosity = self.unittest.as_int('verbosity', 1)
        if args_verbosity is not None:
            self.verbosity = args_verbosity
        # adjust up or down, depending on the difference of these counts
        self.verbosity += args_verbose - args_quiet
        # floor the value at 0 -- verbosity is always a non-negative integer
        self.verbosity = max(self.verbosity, 0)

    def setStartDir(self, args_start_dir=None):
        """
        start dir comes from config and may be overridden by an argument
        """
        self.startDir = self.unittest.as_str('start-dir', '.')
        if args_start_dir is not None:
            self.startDir = args_start_dir

    def prepareSysPath(self):
        """Add code directories to sys.path"""
        tld = self.topLevelDir
        sd = self.startDir
        if tld is None:
            tld = sd
        tld = os.path.abspath(tld)
        util.ensure_importable(tld)
        for libdir in self.libDirs:
            libdir = os.path.abspath(os.path.join(tld, libdir))
            if os.path.exists(libdir):
                util.ensure_importable(libdir)

    # convenience properties
    @property
    def libDirs(self):
        return self.unittest.as_list('code-directories', ['lib', 'src'])

    @property
    def testFilePattern(self):
        return self.unittest.as_str('test-file-pattern', 'test*.py')

    @property
    def testMethodPrefix(self):
        return self.unittest.as_str('test-method-prefix', 'test')

    @property
    def unittest(self):
        return self.get('unittest')

    def isPluginLoaded(self, pluginName):
        """Returns ``True`` if a given plugin is loaded.

        :param pluginName: the name of the plugin module:
                           e.g. "nose2.plugins.layers".

        """
        for plugin in self.plugins:
            if pluginName == plugin.__class__.__module__:
                return True
        return False
