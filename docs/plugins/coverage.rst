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
