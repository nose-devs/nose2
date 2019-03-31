.. image:: https://travis-ci.org/nose-devs/nose2.svg?branch=master
    :target: https://travis-ci.org/nose-devs/nose2
    :alt: Build Status

.. image:: https://coveralls.io/repos/github/nose-devs/nose2/badge.svg?branch=master
    :target: https://coveralls.io/github/nose-devs/nose2?branch=master
    :alt: Coverage Status

.. image:: https://img.shields.io/pypi/v/nose2.svg
    :target: https://pypi.org/project/nose2/
    :alt: Latest PyPI version

 [![Google group : SSFAM News](https://img.shields.io/badge/Google%20Group-SSFAM%20News-blue.svg)](https://groups.google.com/forum/#!forum/ssfam-news)
.. image:: https://img.shields.io/badge/Mailing%20list-discuss%40nose2.io-blue.svg
    :target: https://groups.google.com/a/nose2.io/forum/#!forum/discuss
    :alt: Join discuss@nose2.io

Welcome to nose2
================

``nose2`` is the successor to ``nose``.

It's ``unittest`` with plugins.

``nose2`` is a new project and does not support all of the features of
``nose``. See `differences`_ for a thorough rundown.

nose2's purpose is to extend ``unittest`` to make testing nicer and easier to
understand.

nose2 vs pytest
---------------

``nose2`` may or may not be a good fit for your project.

If you are new to python testing, we encourage you to also consider `pytest`_,
a popular testing framework.

Quickstart
----------

Because ``nose2`` is based on unittest, you can start from the Python Standard
Library's `documentation for unittest <https://docs.python.org/library/unittest.html>`_
and then use nose2 to add value on top of that.

``nose2`` looks for tests in python files whose names start with ``test`` and
runs every test function it discovers.

Here's an example of a simple test, written in typical unittest style:

.. code-block:: python

    # in test_simple.py
    import unittest

    class TestStrings(unittest.TestCase):
        def test_upper(self):
            self.assertEqual("spam".upper(), "SPAM")

You can then run this test like so::

    $ nose2 -v
    test_upper (test_simple.TestStrings) ... ok

    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    OK

However, ``nose2`` supports more testing configuration and provides more tools
than ``unittest`` on its own.

For example, this test exercises just a few of ``nose2``'s features:

.. code-block:: python

    # in test_fancy.py
    from nose2.tools import params

    @params("Sir Bedevere", "Miss Islington", "Duck")
    def test_is_knight(value):
        assert value.startswith('Sir')

and then run this like so::

    $ nose2 -v --pretty-assert
    test_fancy.test_is_knight:1
    'Sir Bedevere' ... ok
    test_fancy.test_is_knight:2
    'Miss Islington' ... FAIL
    test_fancy.test_is_knight:3
    'Duck' ... FAIL

    ======================================================================
    FAIL: test_fancy.test_is_knight:2
    'Miss Islington'
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/mnt/ebs/home/sirosen/tmp/test_fancy.py", line 6, in test_is_knight
        assert value.startswith('Sir')
    AssertionError

    >>> assert value.startswith('Sir')

    values:
        value = 'Miss Islington'
        value.startswith = <built-in method startswith of str object at 0x7f3c3172f430>
    ======================================================================
    FAIL: test_fancy.test_is_knight:3
    'Duck'
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/mnt/ebs/home/sirosen/tmp/test_fancy.py", line 6, in test_is_knight
        assert value.startswith('Sir')
    AssertionError

    >>> assert value.startswith('Sir')

    values:
        value = 'Duck'
        value.startswith = <built-in method startswith of str object at 0x7f3c3172d490>
    ----------------------------------------------------------------------
    Ran 3 tests in 0.001s

    FAILED (failures=2)

Full Docs
---------

Full documentation for ``nose2`` is available at `docs.nose2.io`_

Contributing
------------

If you want to make contributions, please read the `contributing`_ guide.

.. _differences: https://nose2.readthedocs.io/en/latest/differences.html

.. _pytest: http://pytest.readthedocs.io/en/latest/

.. _contributing: https://github.com/nose-devs/nose2/blob/master/contributing.rst

.. _docs.nose2.io: https://docs.nose2.io/en/latest/
