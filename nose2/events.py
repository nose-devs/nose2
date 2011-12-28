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



class Event(object):
    pass


class StartTestEvent(Event):
    pass


class TestReport(Event):
    pass
