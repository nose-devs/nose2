"""
Adapted from unittest2/events.py from the unittest2 plugins branch.

This module contains some code copied from unittest2/events.py and other
code developed in reference to that module and others within unittest2.

unittest2 is Copyright (c) 2001-2010 Python Software Foundation; All
Rights Reserved. See: http://docs.python.org/license.html

"""
import logging

import six

from nose2 import config

log = logging.getLogger(__name__)


class PluginMeta(type):
    def __call__(cls, *args, **kwargs):
        session = kwargs.pop('session', None)
        instance = object.__new__(cls, *args, **kwargs)
        instance.session = session
        if session is not None:
            configSection = getattr(instance, 'configSection', None)
            if configSection is not None:
                instance.config = session.get(configSection)
        else:
            instance.config = config.Config([])
        instance.__init__(*args, **kwargs)
        return instance


class Plugin(six.with_metaclass(PluginMeta)):

    def register(self):
        """Add myself to the plugins that get called"""
        pass

    def addOption(self, callback, short_opt, long_opt, help_text=None):
        """Add command-line option"""
        pass


class Hook(object):
    def __init__(self, method):
        self.method = method
        self.plugins = []

    def __call__(self, event):
        for plugin in self.plugins[:]:
            result = getattr(plugin, self.method)(event)
            if event.handled:
                return result

    def append(self, plugin):
        self.plugins.append(plugin)


class PluginInterface(object):
    def __init__(self):
        self.hooks = {}

    def register(self, method, plugin):
        self.hooks.setdefault(method, Hook(method)).append(plugin)

    def __getattr__(self, attr):
        return self.hooks.setdefault(attr, Hook(attr))


class Event(object):
    def __init__(self, session=None, **kw):
        self.handled = False
        self.session = session
        self.info = {}
        super(Event, self).__init__(**kw)

    def message(self, message, verbosity=(1, 2)):
        if self.session:
            self.session.message(message, verbosity)
        log.warning("Unable to send message %s: no session", message)


class PluginsLoadedEvent(Event):
    def __init__(self, pluginsLoaded, **kw):
        self.pluginsLoaded = pluginsLoaded
        super(PluginsLoadedEvent, self).__init__(**kw)


class StartTestEvent(Event):
    pass


class LoadFromModuleEvent(Event):
    def __init__(self, loader, module, **kw):
        self.loader = loader
        self.module = module
        self.extraTests = []
        super(LoadFromModuleEvent, self).__init__(**kw)


class LoadFromNamesEvent(Event):
    def __init__(self, loader, names, module, **kw):
        self.loader = loader
        self.names = names
        self.module = module
        self.extraTests = []
        super(LoadFromNamesEvent, self).__init__(**kw)


class HandleFileEvent(Event):
    def __init__(self, loader, name, path, pattern,
                    top_level_directory, **kw):
        self.extraTests = []
        self.path = path
        self.loader = loader
        self.name = name
        # note: pattern may be None if not called during test discovery
        self.pattern = pattern
        self.top_level_directory = top_level_directory
        super(HandleFileEvent, self).__init__(**kw)

class TestReport(Event):
    pass
