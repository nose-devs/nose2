===================
Documenting plugins
===================

You should do it. Nobody will use your plugins if you don't. Or if
they do use them, they will curse you whenever things go wrong.

One easy way to document your plugins is to use nose2's `Sphinx`_
extension, which provides an ``autoplugin`` directive that will
produce decent reference documentation from your plugin classes.

To use it, add 'nose2.sphinxext' to the ``extensions`` list in the
``conf.py`` file in your docs directory.

Then add an ``autoplugin`` directive to an rst file, like this::

  .. autoplugin :: mypackage.plugins.PluginClass

This will produce output that includes the config vars your plugin
loads in ``__init__``, as well as any command line options your plugin
registers. This is why you *really* should extract config vars and
register command-line options in ``__init__``.

The output will also include an ``autoclass`` section for your plugin
class, so you can put more narrative documentation in the plugin's
docstring for users to read.

Of course you can, and should, write some words before the reference
docs explaining what your plugin does and how to use it. You can put
those words in the rst file itself, or in the docstring of the module
where your plugin lives.

.. _Sphinx : http://sphinx.pocoo.org/
