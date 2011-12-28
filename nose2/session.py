import sys

from six.moves import configparser

from nose2 import config, events, options

class Session(object):
    """Configuration session.

    Encapsulates all configuration for a given test run.

    """
    def __init__(self):
        self.argparse = options.MultipassOptionParser(prog='nose2')
        self.config = configparser.ConfigParser()
        self.plugins = []

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
        all_  = set(sum(modules, more_plugins)) - exclude
        for module in all_:
            __import__(module)
            self.loadPluginsFromModule(sys.modules[module])

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
            self.plugins.append(cls(session=self))

