===============================
Selecting tests with attributes
===============================

.. note ::

   New in version 0.2

Filter tests by attribute, excluding any tests whose attributes do not
match any of the specified attributes.

Attributes may be simple values or lists, and may be attributes of a
test method (or function), a test case class, or the callable yielded
by a generator test.

Given the following test module, the attrib plugin can be used to
select tests in the following ways (and others!):

.. note ::

   All examples assume the attrib plugin has been activated in a config file:

   .. code-block :: ini

      [unittest]
      plugins = nose2.plugins.attrib


.. literalinclude :: attrib_example.py
   :language: python


Select tests having an attribute
________________________________

Running nose2 like this::

  nose2 -v -A fast

Runs these tests::

  test_fast (attrib_example.Test) ... ok
  test_faster (attrib_example.Test) ... ok

This selects all tests that define the attribute as any True value.


Select tests that do not have an attribute
__________________________________________

Running nose2 like this::

  nose2 -v -A '!fast'

Runs these tests::

  test_slow (attrib_example.Test) ... ok
  test_slower (attrib_example.Test) ... ok

This selects all tests that define the attribute as a False value,
*and those tests that do not have the attribute at all*.


Select tests having an attribute with a particular value
--------------------------------------------------------

Running nose2 like this::

  nose2 -v -A layer=2

Runs these tests::

  test_fast (attrib_example.Test) ... ok
  test_slow (attrib_example.Test) ... ok


This selects all tests that define the attribute with a matching
value. The attribute value of each test case is converted to a string
before comparison with the specified value. Comparison is
case-insensitive.

Select tests having a value in a list attribute
-----------------------------------------------

Running nose2 like this::

  nose2 -v -A flags=red

Runs these tests::

  test_faster (attrib_example.Test) ... ok
  test_slower (attrib_example.Test) ... ok

Since the ``flags`` attribute is a list, this test selects all tests
with the value ``red`` in their ``flags`` attribute. Comparison done
after string conversion and is case-insensitive.


Select tests that do not have a value in a list attribute
---------------------------------------------------------

Running nose2 like this::

  nose2 -v -A '!flags=red'

Runs these tests::

  test_fast (attrib_example.Test) ... ok

The result in this case can be somewhat counter-intuitive. What the
attrib plugin selects when you negate an attribute that is in a list
are only those tests that *have the list attribute* but *without the
value* specified. Tests that do not have the attribute at all are
*not* selected.


Select tests using Python expressions
-------------------------------------

For more complex cases, you can use the :option:`-E` command-line
option to pass a Python expression that will be evaluated in the
context of each test case. Only those test cases where the expression
evaluates to True (and doesn't raise an exception) will be selected.

Running nose2 like this::

  -nose2 -v -E '"blue" in flags and layer > 2'

Runs only one test::

  test_slower (attrib_example.Test) ... ok

.. autoplugin :: nose2.plugins.attrib.AttributeSelector
