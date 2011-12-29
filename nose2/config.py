import sys

from six.moves import configparser

from nose2 import events


TRUE_VALS = set(['1', 't', 'true', 'on', 'yes', 'y'])


class Config(object):
    """Configuration for an element.

    Encapsulates configuration for a single plugin or other element.
    Corresponds to a :ref:`ConfigParser.Section` but provides an
    extended interface for extracting items as a certain type.

    """
    def __init__(self, items):
        self._items = items
        self._mvd = {}
        for k, v in items:
            self._mvd.setdefault(k, []).append(v)

    def __getitem__(self, key):
        return self._mvd[key]

    def as_bool(self, key, default=None):
        try:
            val = self._mvd[key][0].strip()
        except KeyError:
            return default
        except IndexError:
            # setting = -> False
            return False
        return val.lower() in TRUE_VALS

    def as_int(self, key, default=None):
        return self._cast(key, int, default)

    def as_float(self, key, default=None):
        return self._cast(key, float, default)

    def as_str(self, key, default=None):
        return self._cast(key, str, default)

    def as_list(self, key, default=None):
        lines = []
        try:
            vlist = self[key]
        except KeyError:
            return default
        for val in vlist:
            lines.extend(
                line.strip() for line in val.splitlines()
                if line.strip() and not line.strip().startswith('#'))
        return lines

    def _cast(self, key, type_, default):
        try:
            return type_(self._mvd[key][0].strip())
        except (KeyError, IndexError):
            return default


class Session(object):
    """Configuration session.


    Encapsulates all configuration for a given test run.

    """
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.plugins = []

    def get(self, section):
        # FIXME cache these
        items = []
        if self.config.has_section(section):
            items = self.config.items(section)
        return Config(items)

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

