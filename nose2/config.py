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

    def get(self, key, default=None):
        return self.as_str(key, default)

    def _cast(self, key, type_, default):
        try:
            return type_(self._mvd[key][0].strip())
        except (KeyError, IndexError):
            return default
