.. image:: https://results.pre-commit.ci/badge/github/nose-devs/nose2/main.svg
   :target: https://results.pre-commit.ci/latest/github/nose-devs/nose2/main
   :alt: pre-commit.ci status

.. image:: https://github.com/nose-devs/nose2/workflows/build/badge.svg?event=push
    :alt: build status
    :target: https://github.com/nose-devs/nose2/actions?query=workflow%3Abuild

.. image:: https://readthedocs.org/projects/nose2/badge/
    :target: https://nose2.io/
    :alt: Documentation

.. image:: https://img.shields.io/pypi/v/nose2.svg
    :target: https://pypi.org/project/nose2/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/pyversions/nose2.svg
    :alt: Supported Python Versions
    :target: https://pypi.org/project/nose2/

.. image:: https://img.shields.io/badge/Mailing%20list-discuss%40nose2.io-blue.svg
    :target: https://groups.google.com/a/nose2.io/forum/#!forum/discuss
    :alt: Join discuss@nose2.io

Welcome to nose2
================

nose2's extends ``unittest`` to make testing nicer.

nose2 vs nose
-------------

``nose2`` originated as the successor to ``nose``.

``nose2`` is a distinct project and does not support all of the behaviors of ``nose``.
See `differences`_ for a thorough rundown.

nose2 vs pytest
---------------

`pytest`_ is an excellent test framework and we encourage users to consider
it for new projects.

It has a bigger team of maintainers and a larger community of users.

Quickstart
----------

Because ``nose2`` is based on unittest, you can start from the Python Standard
Library's `documentation for unittest <https://docs.python.org/library/unittest.html>`_
and then use nose2 to add value on top of that.

``nose2`` looks for tests in Python files whose names start with ``test`` and
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

Versions and Support
--------------------

Changelog and Version Scheme
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

nose2 versions are numbered ``0.MAJOR.MINOR``. Minor releases contain bugfixes or
smaller features. Major features or backwards incompatible changes are done in
major releases.

For a full description of all past versions and changes, see the `changelog`_.

Python Versions
~~~~~~~~~~~~~~~

nose2 requires Python 3.

It supports all versions currently supported by the CPython team, and also aims
to support PyPy and cpython betas.

Python 2
********

Python 2 is no longer supported. The `0.12.x line of releases <py2line>`_
contains the last versions which supported Python 2.

Users of Python 2 should understand that Python 2 is EOL and the Python 2
support line for ``nose2`` is similarly considered EOL.

.. note::

    Fixes to 0.12.x may still be accepted on an as-needed basis for a short
    while as the python3-only line of releases gets started.

Contributing
------------

If you want to make contributions, please read the `contributing`_ guide.

.. _py2line: https://github.com/nose-devs/nose2/tree/0.12.x-line

.. _differences: https://docs.nose2.io/en/latest/differences.html

.. _changelog: https://docs.nose2.io/en/latest/changelog.html

.. _pytest: http://pytest.readthedocs.io/en/latest/

.. _contributing: https://github.com/nose-devs/nose2/blob/main/contributing.rst

.. _docs.nose2.io: https://docs.nose2.io/en/latest/
