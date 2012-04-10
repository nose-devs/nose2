====================================
Such: a Functional-Test Friendly DSL
====================================

.. note ::

   New in version X.XX

Such is a DSL for writing tests with expensive, nested fixtures --
which typically means functional tests. It requires the layers plugin
(see :doc:`plugins/layers`).

What does it look like?
=======================

Unlike some python testing DSLs, such is just plain old python.

.. literalinclude :: ../nose2/tests/functional/support/such/test_such.py
   :language: python

The tests it defines are unittest tests, and can be used with nose2 with
just the layers plugin. You also have the option of activating a reporting
plugin to provide a more discursive brand of output::

.. literalinclude :: ../nose2/tests/functional/support/such/output.txt

How does it work?
=================

FIXME
