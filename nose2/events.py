class PluginMeta(type):
    def __call__(cls, *args, **kwargs):
        session = kwargs.pop('session', None)
        instance = object.__new__(cls, *args, **kwargs)
        instance.session = session
        if session is not None:
            configSection = getattr(instance, 'configSection', None)
            if configSection is not None:
                instance.config = session.get(configSection)
        instance.__init__(*args, **kwargs)
        return instance


class Plugin(object):
    __metaclass__ = PluginMeta

