from unittest2.util import getObjectFromName

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
        plugin_name = self.arguments[0]
        parent, plugin = getObjectFromName(plugin_name)
        mod_name = plugin_name[0:plugin_name.index(plugin.__name__)-1]

        rst = ViewList()
        rst.append('.. automodule :: %s\n' % mod_name, '<autodoc>')
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

def setup(app):
    app.add_directive('autoplugin', AutoPlugin)
