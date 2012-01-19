Differences: nose2 vs nose vs unittest2
=======================================

nose2 is not nose
-----------------

What's Different
~~~~~~~~~~~~~~~~

Python Versions
^^^^^^^^^^^^^^^

nose supports Python 2.4 and above, but nose2 *only supports Python
2.6, 2.7, 3.2 and pypy*. Unfortunately, supporting Pythons older than
2.6 along with Python 3 in the same codebase is not practical. Since
that is one of the core goals of nose2, support for older versions of
Python had to be sacrificed.

Test Discovery and Loading
^^^^^^^^^^^^^^^^^^^^^^^^^^

nose loads test modules lazily: tests in the first-loaded module are
executed before the second module is imported. *nose2 loads all tests
first, then begins test execution*. This has some important
implications.

First, it means that nose2 does not need a custom importer. nose2
imports test modules with :func:`__import__`.

Second, it means that *nose2 does not support all of the test project
layouts that nose does*. Specifically, projects that look like this
will fail to load tests correctly with nose2::

  .
  `-- tests
      |-- more_tests
      |   `-- test.py
      `-- test.py

To nose's loader, those two test modules look like different
modules. But to nose2's loader, they look the same, and will not load
correctly.

Test Fixtures
^^^^^^^^^^^^^

nose2 supports only the *same levels of fixtures as unittest2*. This
means class level fixtures and module level fixtures are supported,
but *package-level fixtures are not*. In addition, unlike nose, nose2
does not attempt to order tests named on the command-line to group
those with the same fixtures together.


Parameterized and Generator Tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

nose2 supports *more kinds of parameterized and generator tests than
nose*, and supports all test generators in test functions, test
classes, and in unittest TestCase subclasses. nose supports them only
in test fuctions and test classes that do not subclass
unittest.TestCase. See: :doc:`plugins/generators` and
:doc:`plugins/parameters` for more.

Configuration
^^^^^^^^^^^^^

nose expects plugins to make all of their configuration parameters
available as command-line options. *nose2 expects almost all
configuration to be done via configuration files*. Plugins should
generally have only one command-line option: the option to activate
the plugin. Other configuration parameters should be loaded from
config files. This allows more repeatable test runs and keeps the set
of command-line options small enough for humans to read. See:
:doc:`configuration` for more.

Plugin Loading
^^^^^^^^^^^^^^

nose uses setuptools entry points to find and load plugins. nose2
does not. Instead, *nose2 requires that all plugins be listed in config
files*. This ensures that no plugin is loaded into a test system just
by virtue of being installed somewhere, and makes it easier to include
plugins that are part of the project under test. See:
:doc:`configuration` for more.

Limited support for ``python setup.py test``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

nose2 supports setuptools' ``python setup.test`` command, but via very
different means than nose. To avoid the internal complexity forced on
nose by the fact that the setuptools test command can't be configured
with a custom test runner, when run this way, *nose2 essentially
hijacks the test running process*. The "test suite" that
:func:`nose2.collector.collector` returns actually *is* a test runner,
cloaked inside of a test case. It loads and runs tests as normal,
setting up its own test runner and test result, and calls sys.exit()
itself -- completely bypassing the test runner and test result that
setuptools/unittest create. This may be incompatible with some
projects.

New Plugin API
^^^^^^^^^^^^^^

nose2 implements a new plugin API based on the work done by Michael
Foord in unittest2's plugins branch. This API is greatly superior to
the one in nose, especially in how it allows plugins to interact with
each other. But it is different enough from the API in nose that
supporting nose plugins in nose2 will not be practical: *plugins must
be rewritten to work with nose2*. See: :doc:`dev/writing_plugins` for more.

Missing Plugins
^^^^^^^^^^^^^^^

*nose2 does not (yet) include some of the more commonly-used plugins
in nose*, including test coverage, xunit output and filtering tests
using attributes. Most of these should arrive in future
releases. However, some of nose's builtin plugins cannot be ported to
nose2 due to differences in internals. See: :doc:`plugins` for
information on the plugins built in to nose2.

Internals
^^^^^^^^^

nose wraps or replaces everything in unittest. nose2 does a bit less:
*it does not wrap TestCases*, and does not wrap the test result class
with a result proxy. nose2 does subclass TestProgram, and install its
own loader, runner and result classes. It does this unconditionally,
rather than allowing arguments to TestProgram.__init__() to specify
the test loader and runner. See :doc:`dev/internals` for more
information.

License
^^^^^^^

While nose was LGPL, nose2 is BSD licensed. This change was made at
the request of the majority of nose contributors.

What's the Same
~~~~~~~~~~~~~~~

Philosophy
^^^^^^^^^^

nose2 has the same goals as nose: to extend unittest to make testing
nicer and easier to understand. It aims to give developers
flexibility, power and transparency, so that common test scenarios
require no extra work, and uncommon test scenarios can be supported
with minimal fuss and magic.

People
^^^^^^

nose2 is being developed by the same people who maintain nose.

nose2 is not (exactly) unittest2/plugins
----------------------------------------

nose2 is based on the unittest2 plugins branch, but differs from it in
several substantial ways. The *event api not exactly the same* because
nose2 can't replace unittest.TestCase, and *does not configure the test
run or plugin set globally*. nose2 also has a *wholly different
reporting API* from unittest2's plugins, one which we feel better
supports some common cases (like adding extra information to error
output). nose2 also *defers more work to plugins* than unittest2: the
test loader, runner and result are just plugin callers, and all of the
logic of test discovery, running and reporting is implemented in
plugins. This means that unlike unittest2, *nose2 includes a
substantial set of plugins that are active by default*.
