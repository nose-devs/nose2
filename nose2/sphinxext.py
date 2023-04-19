import types

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.statemachine import ViewList

from nose2 import events, plugins, session, util

AD = "<autodoc>"
__unittest = True


class AutoPlugin(Directive):
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = False
    has_content = False
    option_spec = {"module": directives.unchanged}

    def run(self):
        plugin_name = self.arguments[0]
        parent, plugin = util.object_from_name(plugin_name)
        if isinstance(plugin, types.ModuleType):
            # document all plugins in module
            module = plugin
            mod_name = module.__name__
            plugins = self.plugins(module)

        else:
            if "module" in self.options:
                mod_name = self.options["module"]
            else:
                mod_name = plugin_name[0 : plugin_name.index(plugin.__name__) - 1]
            plugins = [plugin]

        rst = ViewList()
        if mod_name:
            rst.append(".. automodule :: %s\n" % mod_name, AD)
            rst.append("", AD)

        for plug in plugins:
            self.document(rst, plug)

        # parse rst and generate new nodelist
        state = self.state
        node = nodes.section()
        node.document = state.document
        surrounding_title_styles = state.memo.title_styles
        surrounding_section_level = state.memo.section_level
        state.memo.title_styles = []
        state.memo.section_level = 0
        state.nested_parse(rst, 0, node, match_titles=1)
        state.memo.title_styles = surrounding_title_styles
        state.memo.section_level = surrounding_section_level

        return node.children

    def document(self, rst, plugin):
        ssn = session.Session()
        ssn.configClass = ssn.config = config = ConfigBucket()
        ssn.pluginargs = opts = OptBucket()
        plugin_name = plugin.__name__
        config = ssn.config
        obj = plugin(session=ssn)
        try:
            obj.pluginsLoaded(events.PluginsLoadedEvent([obj]))
        except AttributeError:
            pass

        # config options
        if config.vars:
            self.add_config(rst, config, plugin)

        # command-line options
        if opts.opts:
            self.headline(rst, "Command-line options")
            for opt in opts:
                for line in opt.options():
                    rst.append(line, AD)
                rst.append("", AD)

        # class __doc__
        self.headline(rst, "Plugin class reference: %s" % plugin_name)
        rst.append(".. autoclass :: %s" % plugin_name, AD)
        rst.append("   :members:", AD)
        rst.append("", AD)

    def add_config(self, rst, config, plugin):
        # add docs on enabling non-default plugins
        plugin_modname = plugin.__module__
        if plugin_modname not in plugins.DEFAULT_PLUGINS:
            self.headline(rst, "Enable this Plugin")
            rst.append("This plugin is built-in, but not loaded by default.", AD)
            rst.append("", AD)
            rst.append(
                "Even if you specify ``always-on = True`` in the "
                "configuration, it will not run unless you also enable it. "
                "You can do so by putting the following in a "
                ":file:`unittest.cfg` or :file:`nose2.cfg` file",
                AD,
            )
            rst.append("", AD)
            rst.append(".. code-block:: ini", AD)
            rst.append("", AD)
            rst.append("  [unittest]", AD)
            rst.append("  plugins = %s" % plugin_modname, AD)
            rst.append("", AD)
            rst.append(
                "The ``plugins`` parameter may contain a list of plugin "
                "names, including ``%s``" % plugin_modname,
                AD,
            )
            rst.append("", AD)

        headline = "Configuration [%s]" % config.section
        self.headline(rst, headline)

        for var in sorted(config.vars.keys()):
            info = config.vars[var]
            rst.append(".. rst:configvar :: %s" % var, AD)
            rst.append("  ", AD)
            rst.append("  :Default: {default}".format(**info), AD)
            rst.append("  :Type: {type}".format(**info), AD)
            rst.append("", AD)

        self.headline(rst, "Sample configuration", "-")
        rst.append(
            "The default configuration is equivalent to including "
            "the following in a :file:`unittest.cfg` file.",
            AD,
        )
        rst.append("", AD)
        rst.append(".. code-block:: ini", AD)
        rst.append("  ", AD)
        rst.append("  [%s]" % config.section, AD)
        for var in sorted(config.vars.keys()):
            info = config.vars[var]
            entry = "  %s = " % (var)
            if info["type"] == "list":
                if info["default"]:
                    pad = " " * len(entry)
                    entry = "{}{}".format(entry, info["default"][0])
                    rst.append(entry, AD)
                    for val in info["default"][1:]:
                        rst.append(f"{pad}{val}", AD)
                else:
                    rst.append(entry, AD)
            elif info["default"] is not None:
                entry = "{}{}".format(entry, info["default"])
                rst.append(entry, AD)
        rst.append("", AD)

    def headline(self, rst, headline, level="="):
        rst.append(headline, AD)
        rst.append(level * len(headline), AD)
        rst.append("", AD)

    def plugins(self, module):
        for _, item in util.iter_attrs(module):
            if not isinstance(item, type):
                continue
            if issubclass(item, events.Plugin):
                yield item


def setup(app):
    app.add_directive("autoplugin", AutoPlugin)
    app.add_object_type("configvar", "config", "pair: %s; configvar")


DEFAULT = object()


class ConfigBucket:
    def __init__(self):
        self.section = None
        self.vars = {}

    def __call__(self, items):
        self.vars = dict(items)
        return self

    def has_section(self, section):
        self.section = section
        return False

    def items(self):
        return self.vars.items()

    def as_bool(self, item, default=DEFAULT):
        self.vars[item] = {"type": "boolean", "default": default}
        return default

    as_tri = as_bool

    def as_int(self, item, default=DEFAULT):
        self.vars[item] = {"type": "integer", "default": default}
        return default

    def as_float(self, item, default=DEFAULT):
        self.vars[item] = {"type": "float", "default": default}
        return default

    def as_str(self, item, default=DEFAULT):
        self.vars[item] = {"type": "str", "default": default}
        return default

    def as_list(self, item, default=DEFAULT):
        self.vars[item] = {"type": "list", "default": default}
        return default

    def __getitem__(self, item):
        self.vars[item] = {"type": None, "default": DEFAULT}

    def get(self, item, default=DEFAULT):
        self.vars[item] = {"type": None, "default": default}
        return default


class OptBucket:
    def __init__(self, doc=None, prog="nosetests"):
        self.seen = set()
        self.opts = []
        self.doc = doc
        self.prog = prog

    def __iter__(self):
        return iter(self.opts)

    def format_help(self):
        return self.doc.replace("%prog", self.prog).replace(":\n", "::\n")

    def add_argument(self, *arg, **kw):
        if arg not in self.seen:
            self.opts.append(Opt(*arg, **kw))
            self.seen.add(arg)

    def __call__(self, callback, opt=None, longOpt=None, help=None):
        opts = []
        if opt is not None:
            opts.append("-" + opt)
        if longOpt is not None:
            opts.append("--" + longOpt)
        self.add_option(*opts, help=help)


class Opt:
    def __init__(self, *arg, **kw):
        self.opts = arg
        self.action = kw.pop("action", None)
        self.default = kw.pop("default", None)
        self.metavar = kw.pop("metavar", None)
        self.help = kw.pop("help", None)

    def options(self):
        buf = []
        for optstring in self.opts:
            desc = optstring
            if self.action not in ("store_true", "store_false", None):
                desc += " %s" % self.meta(optstring)
            buf.append(desc)
            res = [".. cmdoption :: " + ", ".join(buf)]
            if self.help:
                res.append("")
                res.append("   %s" % self.help)
            res.append("")
        return res

    def meta(self, optstring):
        # FIXME optparser default metavar?
        return self.metavar or "DEFAULT"
