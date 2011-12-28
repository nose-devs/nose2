import six

from nose2 import config

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
