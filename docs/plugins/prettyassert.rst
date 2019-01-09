==============================
Use assert statements in tests
==============================

.. autoplugin :: nose2.plugins.prettyassert.PrettyAssert

assert statement inspection
---------------------------

The prettyassert plugin works by inspecting the stack frame which raised an
`AssertionError`. Unlike pytest's assertion rewriting code, it does not modify
the built-in `AssertionError`.

As a result, it is somewhat limited in its capabilities -- it
can only report the *bound* values from that stack frame. That means that this
type of statement works well:

.. code-block:: python

    x = f()
    y = g()
    assert x == y

but this type of statement does not:

.. code-block:: python

    assert f() == g()

It will still run, but the prettyassert will tell you that `f` and `g` are
functions, not what they evaluated to. This is probably not what you want.

attribute resolution
--------------------

The assertion inspection will resolve attributes, so that expressions like this
will work as well:

.. code-block:: python

    assert x.foo == 1

But note that the attribute `x.foo` will be resolved *twice* in this case, if
the assertion fails. Once when the assertion is evaluated, and again when it is
inspected.

As a result, properties with dynamic values may not behave as expected under
prettyassert inspection.
