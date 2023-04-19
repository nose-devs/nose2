Contributing to nose2
=====================

Please do!

The Basics
----------

nose2 is hosted on `github`_ and uses GitHub for issue tracking.

Please report issues and make feature requests here:
https://github.com/nose-devs/nose2/issues

Code Contributions
------------------

The main rule is: *code changes should include tests.*

If you aren't sure how to add tests, or you don't know why existing tests fail
on your changes, that's okay! Submit your patch and ask for help testing it.

Local Dev Requirements
++++++++++++++++++++++

To run the tests you must have `tox`_  installed.

Optional but useful tools include ``make`` and `pre-commit`_.

Running Tests
+++++++++++++

To run all tests: ::

    $ tox

To run linting checks: ::

    $ tox -e lint

You can also use ``make test`` and ``make lint`` for these.

Linting
+++++++

nose2 uses `black`_ and `ruff`_ to enforce code formatting and linting and
`pre-commit`_ to run these tools.

For the best development experience, we recommend setting up integrations with
your editor and git.

Running ``pre-commit`` as a git hook is optional. To configure it, you must
have ``pre-commit`` installed and run:

.. code-block:: bash

    $ pre-commit install

.. note::
    If you need to bypass pre-commit hooks after setting this up, you can commit
    with ``--no-verify``

.. _black: https://black.readthedocs.io/
.. _github: https://github.com/nose-devs/nose2
.. _pre-commit: https://pre-commit.com/
.. _ruff: https://beta.ruff.rs/docs/
.. _tox: http://pypi.python.org/pypi/tox
