=================================================
Running Tests in Parallel with Multiple Processes
=================================================

.. note ::

   New in version 0.3

Use the ``mp`` plugin to enable distribution of tests across multiple
processes. Doing this may speed up your test run if your tests are
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

  nose2 --plugin=nose2.plugins.mp

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
   ``processes`` or pass :option:`-N`, the number of processes
   defaults to the number of CPUs available. Also note that a value of 0 will
   set the actual number of processes to the number of CPUs on the computer.

Should one wish to specify the use of internet sockets for
interprocess communications, specify the ``bind_address``
setting in the ``[multiprocess]`` section of the config file,
for example::

  [multiprocess]
  bind_address = 127.0.0.1:1024

This will bind to port 1024 of ``127.0.0.1``.  Also::

  [multiprocess]
  bind_address = 127.1.2.3

will bind to any random open port on ``127.1.2.3``.  Any internet
address or host-name which python can recognize as such, bind, *and*
connect is acceptable.  While ``0.0.0.0`` can be use for listening,
it is not necessarily an address to which the OS can connect.  When
the port address is ``0`` or omitted, a random open port is used.  If
the setting is omitted or blank, then sockets are not used unless
nose is being executed on Windows.  In which case, an address on
the loop back interface and a random port are used.  Whenever used,
processes employ a random shared key for authentication.

Guidelines for Test Authors
---------------------------

Not every test suite will work well, or work at all, when run in
parallel. For some test suites, parallel execution makes no sense. For
others, it will expose bugs and ordering dependencies in test cases and
test modules.

Overhead Cost
~~~~~~~~~~~~~

Starting subprocesses and dispatching tests takes time. A test run
that includes a relatively small number of tests that are not I/O or
CPU bound (or calling ``time.sleep()``) is likely to be *slower* when run
in parallel.

As of this writing, for instance, nose2's test suite
takes about 10 times as long to run when using ``multiprocessing``, due to
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
order and in different processes. Some test suites have ordering
dependencies, intentional or not, and those that do will fail randomly
when run with this plugin.

Guidelines for Plugin Authors
-----------------------------

The MultiProcess plugin is designed to work with other plugins, but
other plugins may have to return the favor, especially if they load
tests or care about something that happens *during* test execution.


New Methods
~~~~~~~~~~~

The ``MultiProcess`` plugin adds a few plugin hooks that other plugins can
use to set themselves up for multiprocess test runs. Plugins don't
have to do anything special to register for these hooks; just
implement the methods as normal.

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

   Plugins can customize test execution here in the same way as in
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

The ``MultiProcess`` plugin's new hooks come with custom event classes.

.. autoclass :: nose2.plugins.mp.RegisterInSubprocessEvent
   :members:

.. autoclass :: nose2.plugins.mp.SubprocessEvent
   :members:

Stern Warning
~~~~~~~~~~~~~

All event attributes, *including ``event.metadata``, must be
pickleable*. If your plugin sets any event attributes or puts anything
into ``event.metadata``, it is your responsibility to ensure that
anything you can possibly put in is pickleable.

Do I Really Care?
~~~~~~~~~~~~~~~~~

If you answer *yes* to any of the following questions, then your
plugin will not work with multiprocess testing without modification:

* Does your plugin load tests?
* Does your plugin capture something that happens during test execution?
* Does your plugin require user interaction during test execution?
* Does your plugin set executeTests in startTestRun?

Here's how to handle each of those cases.

Loading Tests
^^^^^^^^^^^^^

* Implement :func:`registerInSubprocess` as suggested to enable your
  plugin in the test runner processes.

Capturing Test Execution State
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Implement :func:`registerInSubprocess` as suggested to enable your
  plugin in the test runner processes.

* Be wary of setting ``event.metadata`` unconditionally. Your plugin
  will execute in the main process and in the test runner processes,
  and will see :func:`setTestOutcome` and :func:`testOutcome` events
  *in both processes*. If you unconditionally set a key in
  ``event.metadata``, the plugin instance in the main process will
  overwrite anything set in that key by the instance in the
  subprocess.

* If you need to write something to a file, implement
  :func:`stopSubprocess` to write a file in each test runner process.

Overriding Test Execution
^^^^^^^^^^^^^^^^^^^^^^^^^

* Implement :func:`registerInSubprocess` as suggested to enable your
  plugin in the test runner processes and make a note that your plugin
  is running under a multiprocess session.

* When running multiprocess, *do not* set ``event.executeTests`` in
  :func:`startTestRun` -- instead, set it in :func:`startSubprocess`
  instead. This will allow the multiprocess plugin to install its test
  executor in the main process, while your plugin takes over test
  execution in the test runner subprocesses.

Interacting with Users
^^^^^^^^^^^^^^^^^^^^^^

* You are probably safe because as a responsible plugin author you are
  already firing the interaction hooks (:func:`beforeInteraction`,
  :func:`afterInteraction`) around your interactive bits, and skipping
  them when the :func:`beforeInteraction` hook returns ``False`` and sets
  ``event.handled``.

  If you're not doing that, start!

Possible Issues On Windows
--------------------------

On windows, there are a few known bugs with respect to multiprocessing.

Python on windows does not use fork().  It bootstraps from a
separate interpreter invocation.  In certain contexts, the "value" for
a parameter will be taken as a "count" and subprocess use this to build
the flag for the command-line.  E.g., If this value is 2 billion
(like a hash seed), subprocess.py may attempt to built a 2gig string,
and possibly throw a MemoryError exception.  The related bug is
http://bugs.python.org/issue20954.

Reference
---------

.. autoplugin :: nose2.plugins.mp.MultiProcess
