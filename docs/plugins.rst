=================
Plugins for nose2
=================

Built in and Loaded by Default
==============================

These plugins are loaded by default. To exclude one of these plugins
from loading, add the plugin's fully qualified module name to the
``exclude-plugins`` list in a config file's ``[unittest]`` section,
or pass the plugin module with the ``--exclude-plugin`` argument
on the command line. You can also pass plugin module names to exclude to a
:class:`nose2.main.PluggableTestProgram` using the ``excludePlugins``
keyword argument.

.. toctree::
   :maxdepth: 2

   plugins/discovery
   plugins/functions
   plugins/generators
   plugins/parameters
   plugins/testcases
   plugins/testclasses
   plugins/loadtests
   plugins/dundertests
   plugins/result
   plugins/buffer
   plugins/debugger
   plugins/failfast
   plugins/logcapture
   plugins/coverage
   plugins/prettyassert


Built in but *not* Loaded by Default
====================================

These plugins are available as part of the nose2 package but *are not
loaded by default*. To load one of these plugins, add the plugin module
name (as dot-separated, fully qualified name) to the ``plugins`` list
in a config file's ``[unittest]``
section, or pass the plugin module with the ``--plugin`` argument on
the command line. You can also pass plugin module names to a
:class:`nose2.main.PluggableTestProgram` using the ``plugins`` keyword
argument.

.. toctree::
   :maxdepth: 2

   plugins/junitxml
   plugins/attrib
   plugins/mp
   plugins/layers
   plugins/doctests
   plugins/outcomes
   plugins/collect
   plugins/testid
   plugins/prof
   plugins/printhooks
   plugins/eggdiscovery


Third-party Plugins
===================

If you are a plugin author, please add your plugin to the list on the
`nose2 wiki`_. If you are looking for more plugins, check that list!

.. _nose2 wiki : https://github.com/nose-devs/nose2/wiki/Plugins
