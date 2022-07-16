=======================
Test coverage reporting
=======================

.. autoplugin :: nose2.plugins.coverage.Coverage

Differences From coverage
-------------------------

The ``coverage`` tool is the basis for nose2's coverage reporting. nose2 will
seek to emulate ``coverage`` behavior whenever possible, but there are known
cases where this is not feasible.

If you need the exact behaviors of ``coverage``, consider having ``coverage``
invoke ``nose2``.

Otherwise, please be aware of the following known differences:

- The ``fail_under`` parameter results in an exit status of 2 for ``coverage``,
  but an exit status of 1 for ``nose2``

Compatibility with mp plugin
----------------------------

The ``coverage`` and ``mp`` plugins may be used in conjunction to enable
multiprocess testing with coverage reporting.

Special instructions:

- Due to the way the plugin is reloaded in subprocesses, command-line options
  for the ``coverage`` plugin have no effect. If you need to change any
  ``coverage`` plugin options, use a configuration file.
- Do *not* use the ``concurrency`` option within a ``.coveragerc`` file ; this
  interferes with the ``coverage`` plugin, which automatically handles
  multiprocess coverage reporting.
