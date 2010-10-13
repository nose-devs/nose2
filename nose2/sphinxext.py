from unittest2 import events, util

from docutils import nodes
from docutils.statemachine import ViewList
from docutils.parsers.rst import Directive


class AutoPlugin(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    has_content = False
    option_spec = {}

    def run(self):
        config = ConfigBucket()
        opts = OptBucket()
        self._patch(config, opts)
        try:
            plugin_name = self.arguments[0]
            parent, plugin = util.getObjectFromName(plugin_name)
            # FIXME this is too naive
            mod_name = plugin_name[0:plugin_name.index(plugin.__name__)-1]

            rst = ViewList()
            rst.append('.. automodule :: %s\n' % mod_name, '<autodoc>')
            rst.append('', '<autodoc>')

            obj = plugin()
            try:
                obj.pluginsLoaded(events.PluginsLoadedEvent())
            except AttributeError:
                pass

            # command-line options
            print config.vars

            # config options
            print [opt.options() for opt in opts]

            # class __doc__
            rst.append(' .. autoclass :: %s\n' % plugin_name, '<autodoc>')
            rst.append('', '<autodoc>')

            print rst

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
        finally:
            self._unpatch()

    def _patch(self, config, opts):
        self._getConfig = events.getConfig
        self._addOption = events.addOption
        events.getConfig = config
        events.addOption = opts

    def _unpatch(self):
        events.getConfig = self._getConfig
        events.addOption = self._addOption


def setup(app):
    app.add_directive('autoplugin', AutoPlugin)


DEFAULT = object()

class ConfigBucket(object):
    def __init__(self):
        self.section = None
        self.vars = {}

    def __call__(self, section):
        self.section = section
        self.vars = {}
        return self

    def as_bool(self, item, default=DEFAULT):
        self.vars[item] = {'type': 'boolean',
                           'default': default}
    as_tri = as_bool

    def as_int(self, item, default=DEFAULT):
        self.vars[item] = {'type': 'integer',
                           'default': default}
    def as_float(self, item, default=DEFAULT):
        self.vars[item] = {'type': 'float',
                           'default': default}
    def as_str(self, item, default=DEFAULT):
        self.vars[item] = {'type': 'str',
                           'default': default}
    def as_list(self, item, default=DEFAULT):
        self.vars[item] = {'type': 'list',
                           'default': default}
    def __getitem__(self, item):
        self.vars[item] = {'type': None,
                           'default': DEFAULT}
    def get(self, item, default=DEFAULT):
        self.vars[item] = {'type': None,
                           'default': default}


class OptBucket(object):
    def __init__(self, doc=None, prog='nosetests'):
        self.opts = []
        self.doc = doc
        self.prog = prog

    def __iter__(self):
        return iter(self.opts)

    def format_help(self):
        return self.doc.replace('%prog', self.prog).replace(':\n', '::\n')

    def add_option(self, *arg, **kw):
        self.opts.append(Opt(*arg, **kw))

    def __call__(self, callback, opt=None, longOpt=None, help=None):
        opts = []
        if opt is not None:
            opts.append('-' + opt)
        if longOpt is not None:
            opts.append('--' + longOpt)
        self.add_option(*opts, help=help)


class Opt(object):
    def __init__(self, *arg, **kw):
        self.opts = arg
        self.action = kw.pop('action', None)
        self.default = kw.pop('default', None)
        self.metavar = kw.pop('metavar', None)
        self.help = kw.pop('help', None)

    def options(self):
        buf = []
        for optstring in self.opts:
            desc = optstring
            if self.action not in ('store_true', 'store_false'):
                desc += '=%s' % self.meta(optstring)
            buf.append(desc)
        return '.. cmdoption :: ' + ', '.join(buf)

    def meta(self, optstring):
        # FIXME optparser default metavar?
        return self.metavar or 'DEFAULT'
