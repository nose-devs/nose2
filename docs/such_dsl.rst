======================================
 Such: a Functional-Test Friendly DSL
======================================

.. note ::

   New in version 0.4

Such is a DSL for writing tests with expensive, nested fixtures --
which typically means functional tests. It requires the layers plugin
(see :doc:`plugins/layers`).

What does it look like?
=======================

Unlike some python testing DSLs, such is just plain old python.

.. literalinclude :: ../nose2/tests/functional/support/such/test_such.py
   :language: python

The tests it defines are unittest tests, and can be used with nose2
with just the layers plugin. You also have the option of activating a
reporting plugin (:class:`nose2.plugins.layers.LayerReporter`) to
provide a more discursive brand of output:

.. literalinclude :: ../nose2/tests/functional/support/such/output.txt

How does it work?
=================

Such uses the things in python that are most like anonymous code
blocks to allow you to construct tests with meaningful names and
deeply-nested fixtures. Compared to DSLs in languages that do allow
blocks, it is a little bit more verbose -- the block-like decorators
that mark fixture methods and test cases need to decorate *something*,
so each fixture and test case has to have a function definition. You
can use the same function name over and over here, or give each
function a meaningful name.

The set of tests begins with a description of the system under test as
a whole, marked with the ``A`` context manager:

.. code-block :: python

  from nose2.tools import such

  with such.A('system described here') as it:
      # ...

Groups of tests are marked by the ``having`` context manager:

.. code-block :: python

  with it.having('a description of a group'):
      # ...

Within a test group (including the top-level group), fixtures are
marked with decorators:

.. code-block :: python

  @it.has_setup
  def setup():
      # ...

  @it.has_test_setup
  def setup_each_test_case():
      # ...

And tests are likewise marked with the ``should`` decorator:

.. code-block :: python

   @it.should('exhibit the behavior described here')
   def test(case):
       # ...

Test cases may optionally take one argument. If they do, they will be
passed the :class:`unittest.TestCase` instance generated for the
test. They can use this ``TestCase`` instance to execute assert methods,
among other things. Test functions can also call assert methods on the
top-level scenario instance, if they don't take the ``case`` argument:

.. code-block :: python

   @it.should("be able to use the scenario's assert methods")
   def test():
       it.assertEqual(something, 'a value')

   @it.should("optionally take an argument")
   def test(case):
       case.assertEqual(case.attribute, 'some value')

Finally, to actually generate tests, you **must** call ``createTests`` on
the top-level scenario instance:

.. code-block :: python

  it.createTests(globals())

This call generates the :class:`unittest.TestCase` instances for all
of the tests, and the layer classes that hold the fixtures defined in
the test groups. See :doc:`plugins/layers` for more about test
layers.

Running tests
-------------

Since order is often significant in functional tests, **such DSL tests
always execute in the order in which they are defined in the
module**. Parent groups run before child groups, and sibling groups
and sibling tests within a group execute in the order in which they
are defined.

Otherwise, tests written in the such DSL are collected and run just like any
other tests, with one exception: their names. The name of a such test
case is the name of its immediately surrounding group, plus the
description of the test, prepended with ``test ####:``, where ``####``
is the test's (``0`` -indexed) position within its group.

To run a case individually, you must pass in this full name -- usually you'll have to quote it. For example, to run the case ``should do more things``
defined above (assuming the layers plugin is activated by a config
file, and the test module is in the normal path of test collection),
you would run nose2 like this::

  nose2 "test_such.having an expensive fixture.test 0000: should do more things"

That is, for the generated test case, the **group description** is
the **class name**, and the **test case description** is the **test
case name**. As you can see if you run an individual test with the
layer reporter active, all of the group fixtures execute in proper
order when a test is run individually::

  $ nose2 "test_such.having an expensive fixture.test 0000: should do more things"
  A system with complex setup
    having an expensive fixture
      should do more things ... ok

  ----------------------------------------------------------------------
  Ran 1 test in 0.000s

  OK


Reference
=========

.. automodule :: nose2.tools.such
  :members: A, Scenario
