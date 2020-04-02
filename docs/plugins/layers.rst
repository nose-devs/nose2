====================================
Organizing Test Fixtures into Layers
====================================

.. note ::

   New in version 0.4

Layers allow more flexible organization of test fixtures than test-, class- and
module- level fixtures. Layers in nose2 are inspired by and aim to be
compatible with the layers used by Zope's testrunner.

Using layers, you can do things like:

* Implement package-level fixtures by sharing a layer among all test cases in
  the package.

* Share fixtures across tests in different modules without having them run
  multiple times.

* Create a fixture tree deeper than three levels (test, class and module).

* Make fixtures available for other packages or projects to use.

A layer is a *new-style* class that implements at least a ``setUp``
classmethod:

.. code-block:: python

    class Layer(object):
       @classmethod
       def setUp(cls):
           # ...

It may also implement ``tearDown``, ``testSetUp`` and ``testTearDown``, all as
classmethods.

To assign a layer to a test case, set the test case's ``layer`` property:

.. code-block:: python

    class Test(unittest.TestCase):
        layer = Layer

Note that the layer *class* is assigned, not an instance of the layer.
Typically layer classes are not instantiated.

Sub-layers
==========

Layers may subclass other layers:

.. code-block:: python

    class SubLayer(Layer):
        @classmethod
        def setUp(cls):
            # ...

In this case, all tests that belong to the sub-layer also belong to the base
layer. For example for this test case:

.. code-block:: python

    class SubTest(unittest.TestCase):
        layer = SubLayer

The ``setUp`` methods from *both* ``SubLayer`` and ``Layer`` will run before
any tests are run. The superclass's setup will always run before the subclass's
setup. For ``teardown``, the reverse: the subclass's ``teardown`` runs before
the superclass's.

.. warning::

   One important thing to note: layers that subclass other layers *must
   not* call their superclass's ``setUp``, ``tearDown``, etc. The test
   runner will take care of organizing tests so that the superclass's
   methods are called in the right order::

     Layer.setUp ->
       SubLayer.setUp ->
         Layer.testSetUp ->
           SubLayer.testSetUp ->
             TestCase.setUp
               TestCase.run
             TestCase.tearDown
           SubLayer.testTearDown <-
         Layer.testTearDown <-
       SubLayer.tearDown <-
     Layer.tearDown <-

   If a sublayer calls it superclass's methods directly, *those
   methods will be called twice*.


Layer method reference
======================

.. class:: Layer

   Not an actual class, but reference documentation for
   the methods layers can implement. There is no layer
   base class. Layers must be subclasses of :class:`object`
   or other layers.

   .. classmethod:: setUp(cls)

      The layer's ``setUp`` method is called before any tests belonging to
      that layer are executed. If no tests belong to the layer (or one of
      its sub-layers) then the ``setUp`` method will not
      be called.

   .. classmethod:: tearDown(cls)

      The layer's ``tearDown`` method is called after any tests
      belonging to the layer are executed, if the layer's ``setUp``
      method was called and did not raise an exception. It will not
      be called if the layer has no ``setUp`` method, or if that
      method did not run or did raise an exception.

   .. classmethod:: testSetUp(cls[, test])

      The layer's ``testSetUp`` method is called before each test
      belonging to the layer (and its sub-layers). If
      the method is defined to accept an argument, the test case
      instance is passed to the method. The method may also be
      defined to take no arguments.

   .. classmethod:: testTearDown(cls[, test])

      The layer's ``testTearDown`` method is called after each test
      belonging to the layer (and its sub-layers), if
      the layer also defines a ``setUpTest`` method and that method
      ran successfully (did not raise an exception) for this test
      case.

Layers DSL
==========

nose2 includes a DSL for setting up layer-using tests called
"such". Read all about it here: :doc:`../such_dsl`.

Pretty reports
==============

The layers plugin module includes a second plugin that alters test
report output to make the layer groupings more clear. When activated
with the :option:`--layer-reporter` command-line option (or via a config
file), test output that normally looks like this::

  test (test_layers.NoLayer) ... ok
  test (test_layers.Outer) ... ok
  test (test_layers.InnerD) ... ok
  test (test_layers.InnerA) ... ok
  test (test_layers.InnerA_1) ... ok
  test (test_layers.InnerB_1) ... ok
  test (test_layers.InnerC) ... ok
  test2 (test_layers.InnerC) ... ok

  ----------------------------------------------------------------------
  Ran 8 tests in 0.001s

  OK

Will instead look like this::

  test (test_layers.NoLayer) ... ok
  Base
    test (test_layers.Outer) ... ok
    LayerD
      test (test_layers.InnerD) ... ok
    LayerA
      test (test_layers.InnerA) ... ok
    LayerB
      LayerC
        test (test_layers.InnerC) ... ok
        test2 (test_layers.InnerC) ... ok
      LayerB_1
        test (test_layers.InnerB_1) ... ok
      LayerA_1
        test (test_layers.InnerA_1) ... ok

  ----------------------------------------------------------------------
  Ran 8 tests in 0.002s

  OK

The layer reporter plugin can also optionally colorize the keywords
(by default, 'A', 'having', and 'should') in output from tests defined
with the :doc:`such DSL <../such_dsl>`.

If you would like to change how the layer is displayed, set the ``description`` attribute.

.. code-block:: python

  class LayerD(Layer):
      description = '*** This is a very important custom layer description ***'

Now the output will be the following::


  test (test_layers.NoLayer) ... ok
  Base
    test (test_layers.Outer) ... ok
    *** This is a very important custom layer description ***
      test (test_layers.InnerD) ... ok
    LayerA
      test (test_layers.InnerA) ... ok
    LayerB
      LayerC
        test (test_layers.InnerC) ... ok
        test2 (test_layers.InnerC) ... ok
      LayerB_1
        test (test_layers.InnerB_1) ... ok
      LayerA_1
        test (test_layers.InnerA_1) ... ok

  ----------------------------------------------------------------------
  Ran 8 tests in 0.002s

  OK


Warnings and Caveats
====================

Test case order and module isolation
------------------------------------

Test cases that use layers will not execute in the same order as test
cases that do not. In order to execute the layers efficiently, the
test runner must reorganize *all* tests in the loaded test suite to
group those having like layers together (and sub-layers under their
parents). If you share layers across modules this may result in tests
from one module executing interleaved with tests from a different
module.


Mixing layers with ``setUpClass`` and module fixtures
-----------------------------------------------------

**Don't cross the streams.**

The implementation of class- and module-level fixtures in unittest2
depends on introspecting the class hierarchy inside of the
``unittest.TestSuite``. Since the suites that the ``layers`` plugin uses to
organize tests derive from :class:`unittest.BaseTestSuite` (instead of
:class:`unittest.TestSuite`), class- and module- level fixtures in
TestCase classes that use layers will be ignored.

Mixing layers and multiprocess testing
--------------------------------------

In the initial release, *test suites using layers are incompatible with
the multiprocess plugin*. This should be fixed in a future release.


Plugin reference
================

.. autoplugin :: nose2.plugins.layers
