==========================
Loader: Egg Test discovery
==========================


What is Egg Discovery
---------------------

Sometimes Python Eggs are marked as zip-safe and they can be installed zipped,
instead of unzipped in an ``.egg`` folder. See http://peak.telecommunity.com/DevCenter/PythonEggs for more details.
The normal ``nose2.plugins.loader.discovery`` plugin ignores modules located inside zip files.

The Egg Discovery plugin allows nose2 to discover tests within these zipped egg files.

This plugin requires ``pkg_resources`` (from ``setuptools``) to work correctly.


Usage
-----

To activate the plugin, include the plugin module in the plugins list
in ``[unittest]`` section in a config file::

  [unittest]
  plugins = nose2.plugins.loader.eggdiscovery

Or pass the module with the :option:`--plugin` command-line option::

  nose2 --plugin=nose2.plugins.loader.eggdiscovery module_in_egg


Reference
---------

.. autoplugin :: nose2.plugins.loader.eggdiscovery.EggDiscoveryLoader
