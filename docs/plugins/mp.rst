=================================================
Running Tests in Parallel with Multiple Processes
=================================================

.. note ::

   New in version 0.3

Use the ``mp`` plugin to enable distribution of tests across multiple
processes. Doing his may speed up your test run if your tests are
heavily IO or CPU bound. But it *imposes an overhead cost* that is not
trivial, and it *complicates the use of test fixtures* and may *conflict
with plugins that are not designed to work with it*.

Usage
-----

To activate the plugin, include the plugin module in the plugins list
in ``[unittest]`` section in a config file::

  [unittest]
  plugins = nose2.plugins.mp

Or pass the module with the :option:`--plugin` command-line option::

  nose2 --plugin=nose2.plugin.mp

Then configure the number of processes to run. You can do that either
with the :option:`-N` option::

  nose2 -N 2

or by setting ``processes`` in the ``[multiprocess]`` section of a
config file::

  [multiprocess]
  processes = 2

.. note ::

   If you make the plugin always active by setting ``always-on`` in
   the ``[multiprocess]`` section of a config file, but do not set
   ``processes`` or pass :option:`-N`, the number of processes default
   to the number of cpus available.

Caveats for Test Authors
------------------------

Not every test suite will work well, or work at all, when run in
parallel. For some test suites, parallel execution makes no sense. For
others, it will expose bugs and ordering dependencies test cases and
test modules.

Overhead Cost
~~~~~~~~~~~~~

Starting subprocesses and dispatching tests takes time. A test run
that includes a relatively small number of tests that are not IO or
CPU bound (or calling time.sleep()) is likely to be *slower* when run
in parallel. As of this writing, for instance, nose2's test suite
takes about 10 times as long to run when using multiprocessing, due to
the overhead cost.

Shared Fixtures
~~~~~~~~~~~~~~~

The individual test processes do not share state or data after
launch. This means *tests that share a fixture* -- tests that are loaded
from modules where ``setUpModule`` is defined, and tests in test
classes that define ``setUpClass`` -- *must all be dispatched to the
same process at the same time*. So if you use these kinds of fixtures,
your test runs may be less parallel than you expect.

Tests Load Twice
~~~~~~~~~~~~~~~~

Test cases may not be pickleable, so nose2 can't transmit them
directly to its test runner processes. Tests are distributed by
name. This means that *tests always load twice* -- once in the main
process, during initial collection, and then again in the test runner
process, where they are loaded by name. This may be problematic for
some test suites.

Random Execution Order
~~~~~~~~~~~~~~~~~~~~~~

Tests do not execute in the same order when run in parallel. Results
will be returned in effectively random order, and tests in the same
module (*as long as they do not share fixtures*) may execute in any
order and in different processes. Some tests suites have ordering
dependencies, intentional or not, and those that do will fail randomly
when run with this plugin.

Guidelines for Plugin Authors
-----------------------------

The MultiProcess plugin is designed to work with other plugins. But
other plugins may have to return the favor, especially if they load
tests or care about something that happens *during* test execution.


New Methods
~~~~~~~~~~~

.. function :: registerInSubprocess(self, event)

   :param event: :class:`nose2.plugins.mp.RegisterInSubprocessEvent`

   The ``registerInSubprocess`` hook is called after plugin
   registration to enable plugins that need to run in subprocesses to
   register that fact. The most common thing to do, for plugins that
   need to run in subprocesses, is::

         def registerInSubprocess(self, event):
             event.pluginClasses.append(self.__class__)

   It is not required that plugins append their own class. If for some
   reason there is a different plugin class, or set of classes, that
   should run in the test-running subprocesses, add that class or
   those classes instead.

.. function :: startSubprocess(self, event)

   :param event: :class:`nose2.plugins.mp.SubprocessEvent`

   The ``startSubprocess`` hook fires in each test-running subprocess
   after it has loaded its plugins but before any tests are executed.

   Plugins can customize test execution here in the same was as in
   :func:`startTestRun`, by setting ``event.executeTests``, and
   prevent test execution by setting ``event.handled`` to True and
   returning False.

.. function :: stopSubprocess(self, event)

   :param event: :class:`nose2.plugins.mp.SubprocessEvent`

   The ``stopSubprocess`` event fires just before each test running
   subprocess shuts down. Plugins can use this hook for any
   per-process finalization that they may need to do.

   The same event instance is passed to ``startSubprocess`` and
   ``stopSubprocess``, which enables plugins to use that event's
   metadata to communicate state or other information from the
   start to the stop hooks, if needed.

New Events
~~~~~~~~~~

.. autoclass :: nose2.plugins.mp.RegisterInSubprocessEvent
   :members:

.. autoclass :: nose2.plugins.mp.SubprocessEvent
   :members:

Stern Warning
~~~~~~~~~~~~~

* all event fields incl. event.metadata must be pickleable

Do I Really Care?
~~~~~~~~~~~~~~~~~

do you capture something that happens during test execution?

do you load tests?

do you set executeTests in startTestRun?

Reference
---------

.. autoplugin :: nose2.plugins.mp.MultiProcess
