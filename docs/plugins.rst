===============
Builtin Plugins
===============

Loaded by Default
=================

These plugins are loaded by default. To exclude one of these plugins
from loading, add the plugin's module name to the ``exclude-plugins``
list in a config file's ``[unittest]`` section, or pass the plugin
module with the ``--exclude-plugin`` argument on the command line. You
can also pass plugin module names to exclude to a
:class:`nose2.main.PluggableTestProgram` using the ``excludePlugins``
keyword argument.

.. toctree::
   :maxdepth: 2

   plugins/discovery
   plugins/functions
   plugins/generators
   plugins/parameters
   plugins/testcases
   plugins/result
   plugins/buffer
   plugins/debugger
   plugins/failfast
   plugins/logcapture
   plugins/outcomes
   plugins/collect
   plugins/testid


Available
=========

These plugins are available as part of the nose2 package but not
loaded by default. To load these plugins, add the plugin module name
to the ``plugins`` list in a config file's ``[unittest]`` section, or
pass the plugin module with the ``--plugin`` argument on the command
line. You can also pass plugin module names to a
:class:`nose2.main.PluggableTestProgram` using the ``plugins`` keyword
argument.

.. toctree::
   :maxdepth: 2

   plugins/attrib
   plugins/doctests
   plugins/junitxml
   plugins/prof
   plugins/printhooks
