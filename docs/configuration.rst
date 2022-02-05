Configuring nose2
=================

Configuration Files
-------------------

nose2 can be configured via standard, ini-style config files.
The default files are ``unittest.cfg`` and ``nose2.cfg`` in the start directory.

The ini format has sections marked off by brackets ("``[unittest]``") and
``key = value`` pairs within those sections.
When the value is a list, put each value into its own line with proper
indentation ::

    key_expecting_list = value1
                         value2

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

.. rst:configvar :: start-dir

   This option configures the default directory to start discovery.
   The default value is ``"."`` (the current directory where nose2
   is executed). This directory is where nose2 will start looking for
   tests.

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
  start-dir = tests
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
   The module is specified by the (dot-separated) *fully qualified* name.

Examples:

.. code-block :: ini

  [unittest]
  plugins = myproject.plugins.frobulate
            otherproject.contrib.plugins.derper

  exclude-plugins = nose2.plugins.loader.functions
                    nose2.plugins.outcomes


Configuring Plugins
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


Test Runner Tips and Tweaks
---------------------------

Running Tests in a Single Module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use ``nose2.main`` in the same way that ``unittest.main`` (and
``unittest2.main``) have historically worked: to run the tests in a
single module. Just put a block like the following at the end of the
module::

  if __name__ == '__main__':
      import nose2
      nose2.main()

Then *run the module directly* -- In other words, do not run the
``nose2`` script.

Rolling Your Own Runner
~~~~~~~~~~~~~~~~~~~~~~~

You can take more control over the test runner by foregoing the
``nose2`` script and rolling your own. To do that, you just need to
write a script that calls ``nose2.discover``, for instance::

  if __name__ == '__main__':
    import nose2
    nose2.discover()

You can pass several keyword arguments to ``nose2.discover``, all of
which are detailed in the documentation for
:class:`nose2.main.PluggableTestProgram`.

Altering the Default Plugin Set
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To add plugin *modules* to the list of those automatically loaded, you
can pass a list of module names to add (the ``plugins``) argument or
exclude (``excludedPlugins``). You can also subclass
:class:`nose2.main.PluggableTestProgram` and set the class-level
``defaultPlugins`` and ``excludePlugins`` attributes to alter plugin
loading.

When Loading Plugins from Modules is not Enough
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**None of which will help** if you need to register a plugin *instance*
that you've loaded yourself. For that, use the ``extraHooks`` keyword
argument to ``nose2.discover``. Here, you pass in a list of 2-tuples,
each of which contains a hook name and a plugin *instance* to register
for that hook. This allows you to register plugins that need runtime
configuration that is not easily passed in through normal channels --
and also to register *objects that are not nose2 plugins* as hook
targets. Here's a trivial example::

  if __name__ == '__main__':
    import nose2

    class Hello(object):
        def startTestRun(self, event):
            print("hello!")

    nose2.discover(extraHooks=[('startTestRun', Hello())])

This can come in handy when integrating with other systems that expect
you to provide a test runner that they execute, rather than executing
tests yourself (django, for instance).
