Configuring nose2
=================

Configuration Files
-------------------

Most configuration of nose2 is done via config files. These are
standard, .ini-style config files, with sections marked off by
brackets ("``[unittest]``") and ``key = value`` pairs within those sections.

Two command line options, :option:`-c` and :option:`--no-user-config`
may be used to determine which config files are loaded.

.. cmdoption :: -c CONFIG, --config CONFIG

   Config files to load. Default behavior is to look for
   ``unittest.cfg`` and ``nose2.cfg`` in the start directory, as well
   as any user config files (unless :option:`--no-user-config` is
   selected).

.. cmdoption :: --no-user-config

   Do not load user config files. If not specified, in addition to the
   standard config files and any specified with :option:`-c`, nose2
   will look for ``.unittest.cfg`` and ``.nose2.cfg`` in the user's
   $HOME directory.


Configuring Test Discovery
~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``[unittest]`` section of nose2 config files is used to configure
nose2 itself. The following options are available to configure test
discovery:

.. rst:configvar :: code-directories

   This option configures nose2 to add the named directories to
   sys.path and the discovery path. Use this if your project has
   code in a location other than the top level of the project, or the
   directories ``lib`` or ``src``. The value here may be a list: put each
   directory on its own line in the config file.

.. rst:configvar :: test-file-pattern

   This option configures how nose detects test modules. It is a file
   glob.

.. rst:configvar :: test-method-prefix

   This option configures how nose detects test functions and
   methods. The prefix set here will be matched (via simple string
   matching) against the start of the name of each method in test
   cases and each function in test modules.

Examples:

.. code-block :: ini

  [unittest]
  code-directories = source
                     more_source
  test-file-pattern = *_test.py
  test-method-prefix = t


Specifying Plugins to Load
~~~~~~~~~~~~~~~~~~~~~~~~~~

To avoid loading any plugins, use the :option:`--no-plugins`
option. Beware, though: nose2 does all test discovery and loading via
plugins, so unless you are patching in a custom test loader and
runner, when run with :option:`--no-plugins`, nose2 will do nothing.

.. cmdoption :: --no-plugins

   Do not load any plugins. *This kills the nose2.*

To specify plugins to load beyond the builtin plugins automatically
loaded, add a :config:`plugins` entry under the ``[unittest]``
section in a config file.

.. rst:configvar :: plugins

   List of plugins to load. Put one plugin module on each line.

To exclude some plugins that would otherwise be loaded, add an
:config:`exclude-plugins` entry under the ``[unittest]``
section in a config file.

.. rst:configvar :: exclude-plugins

   List of plugins to exclude. Put one plugin module on each line.

.. note ::

   It bears repeating that in both :config:`plugins` and
   :config:`exclude-plugins` entries, you specify the plugin *module*,
   not the plugin *class*.

Examples:

.. code-block :: ini

  [unittest]
  plugins = myproject.plugins.frobulate
            otherproject.contrib.plugins.derper

  exclude-plugins = nose2.plugins.loader.functions
                    nose2.plugins.outcomes


Configuring plugins
-------------------

Most plugins specify a config file section that may be used to
configure the plugin. If nothing else, any plugin that specifies a
config file section can be set to automatically register by including
``always-on = True`` in its config:

.. code-block :: ini

   [my-plugin]
   always-on = True

Plugins may accept any number of other config values, which may be
booleans, strings, integers or lists. A polite plugin will document
these options somewhere. Plugins that want to make use of nose2's
`Sphinx`_ extension as detailed in :doc:`dev/documenting_plugins`
*must* extract all of their config values in their ``__init__``
methods.

.. _Sphinx : http://sphinx.pocoo.org/
