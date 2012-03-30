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

Specifying Tests to Run
~~~~~~~~~~~~~~~~~~~~~~~

Pass *test names* to nose2 on the command line to run individual test
modules, classes, or tests.

A test name consists of a *python object part* and, for generator or
parameterized tests, an *argument part*. The *python object part* is a
dotted name, such as
``pkg1.tests.test_things.SomeTests.test_ok``. The argument
part is separated from the python object part by a colon (":") and
specifies the *index* of the generated test to select, *starting from
1*. For example, ``pkg1.test.test_things.test_params_func:1`` would
select the *first* test generated from the parameterized test
``test_params_func``.

Plugins may provide other means of test selection.

Running Tests with ``python setup.py test``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

nose2 supports distribute/setuptools' ``python setup.py test``
standard for running tests. To use nose2 to run your package's tests,
add the following to your setup.py::

  setup(...
        test_suite='nose2.collector.collector',
        ...
        )

(Not literally. Don't put the '...' parts in.)

Two warnings about running tests this way.

One: because the setuptools test command is limited, nose2 returns a "test
suite" that actually takes over the test running process completely,
bypassing the test result and test runner that call it. This may be
incompatible with some packages.

Two: because the command line arguments to the test command may not
match up properly with nose2's arguments, the nose2 instance started
by the collector *does not accept any command line arguments*. This
means that it always runs all tests, and that you cannot configure
plugins on the command line when running tests this way. As a
workaround, when running under the test command, nose2 will read
configuration from ``setup.cfg`` if it is present, in addition to
``unittest.cfg`` and ``nose2.cfg``. This enables you to put
configuration specific to the setuptools test command in ``setup.cfg``
-- for instance to activate plugins that you would otherwise activate
via the command line.


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
