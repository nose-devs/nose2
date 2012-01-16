Using nose2
===========

Running Tests
-------------

In the simplest case, go to the directory that includes your project
source and run ``nose2`` there::

  nose2

This will discover tests in packages and test directories under that
directory, load them, and run them, then output something like::

  .............................................................................
  ----------------------------------------------------------------------
  Ran 77 tests in 1.897s

  OK

"Test directories" means any directories whose names start with
"test". Within test directories and within any Python packages found
in the starting directory and any source directories in the starting
directory, nose2 will discover test modules and load tests from
them. "Test modules" means any modules whose names start with "test".

Within test modules, nose2 will load tests from
:class:`unittest.TestCase` subclasses, and from test functions
(functions whose names begin with "test").

.. todo ::

   ... and test classes (classes whose names begin with "Test")

To change the place discovery starts, or to change the top-level
importable directory of the project, use the :option:`-s` and
:option:`-t` options.

.. cmdoption :: -s START_DIR, --start-dir START_DIR

   Directory to start discovery. Defaults to the current working
   directory. This directory is where nose2 will start looking for
   tests.

.. cmdoption :: -t TOP_LEVEL_DIRECTORY, --top-level-directory TOP_LEVEL_DIRECTORY, --project-directory TOP_LEVEL_DIRECTORY

   Top-level directory of the project. Defaults to the starting
   directory. This is the directory containing importable modules and
   packages, and is always prepended to sys.path before test discovery
   begins.


Configuration Files
-------------------

Most configuration of nose2 is done via config files. These are
standard, .ini-style config files, with sections marked off by
brackets ("[unittest]") and key = value pairs within those sections.

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


Getting Help
------------

Run::

  nose2 -h

to get help for nose2 itself and all loaded plugins.

::

  usage: nose2 [-s START_DIR] [-t TOP_LEVEL_DIRECTORY] [--config [CONFIG]]
               [--no-user-config] [--no-plugins] [--verbose] [--quiet] [-B] [-D]
               [--collect-only] [--log-capture] [-P] [-h]
               [testNames [testNames ...]]

  positional arguments:
    testNames

  optional arguments:
    -s START_DIR, --start-dir START_DIR
                          Directory to start discovery ('.' default)
    -t TOP_LEVEL_DIRECTORY, --top-level-directory TOP_LEVEL_DIRECTORY, --project-directory TOP_LEVEL_DIRECTORY
                          Top level directory of project (defaults to start dir)
    --config [CONFIG], -c [CONFIG]
                          Config files to load, if they exist. ('unittest.cfg'
                          and 'nose2.cfg' in start directory default)
    --no-user-config      Do not load user config files
    --no-plugins          Do not load any plugins. Warning: nose2 does not do
                          anything if no plugins are loaded
    --verbose, -v
    --quiet
    -h, --help            Show this help message and exit

  plugin arguments:
    Command-line arguments added by plugins:

    -B, --output-buffer   Enable output buffer
    -D, --debugger        Enter pdb on test fail or error
    --collect-only        Collect and output test names, do not run any tests
    --log-capture         Enable log capture
    -P, --print-hooks     Print names of hooks in order of execution
