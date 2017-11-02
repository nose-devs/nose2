Contributing to nose2
=====================

Please do! nose2 cannot move forward without contributions from the
testing community.

If you're unsure how to get started, feel free to ask for help from the nose2
community on `gitter <https://gitter.im/nose2>`_. We welcome contributors with
all levels of experience.

This document is a set of guidelines, not strict rules.
Use your best judgement, and feel free to propose changes to this document
in a pull request.

The Basics
----------

nose2 is hosted on `github`_. Our home there is
https://github.com/nose-devs/nose2. We use github's issue tracking and
collaboration tools *exclusively* for managing nose2's
development. This means:

* Please report issues here: https://github.com/nose-devs/nose2/issues

* Please make feature requests in the same place

* Please submit all patches as github pull requests

Coding Guidelines
-----------------

The main rule is: *any patch that touches code should include tests.*
And of course all tests should pass under all supported versions of Python.

If you aren't sure how to add tests, or you don't know why existing tests fail
on your changes, submit your patch and ask for help testing it.

Tests are easy to run. Just install `tox`_ (``pip install tox``), and run
``tox`` in the nose2 root directory.

Some additional tips for the python and documentation in this project.

- Code should be `pep8`_ compliant
- Where possible, write code which passes ``pyflakes`` linting (consider using
  ``flake8`` to do ``pyflakes`` and ``pep8`` checking)
- For consistency with ``unittest`` please use CamelCase for class names,
  methods, attributes and function parameters that map directly to class
  attributes.
- Try to use raw strings for docstrings -- ensures that ReST won't be
  confused by characters like ``\\``
- For complex functionality, include sample usage in docstrings
- Comment liberally, but don't comment on every line of code
- Use examples very liberally in documentation
- Use double-quotes for strings, except when quoting a string containing
  double-quotes but not containing single quotes
- Use absolute imports everywhere
- Avoid circular imports whenever possible -- given the choice between adding
  a new module or adding a circular import, add the new module
- Import non-``nose2`` modules and packages before importing from within
  ``nose2``
- Think very hard before adding a new dependency -- keep the dependencies of
  ``nose2`` as lightweight as possible

Commit Messages
~~~~~~~~~~~~~~~

A few basic ground rules for what ideal commits should look like.

- No lines over 72 characters
- No GitHub emoji -- use your words
- Reference issues and pull requests where appropriate
- Prefer present tense and imperative mood
  e.g. rather than "added feature foo" (past indicative)
  or "adds feature foo" (present indicative)
  the best option is "add feature foo" (present imperative)

Workflow, Branching and Pull Requests
-------------------------------------

The basic workflow should be to do the work in a topic branch in your fork
then post a pull request for that branch.

Core devs should not merge their own work -- unless it's trivial -- without
giving other developers a chance to review it.

For any pull request,

- *Make sure it meets the standards set in this document*
- *Make sure it merges cleanly*
- *List any issues closed by the pull request*
- *Squash intermediate commits*. Consider using ``git rebase --interactive`` to
  squash typo fixes, aborted implementations, etc.

Reporting Bugs
--------------

The best bug reports are ones which:

- *Check for duplicates*. Do a quick search to try to make sure you aren't
  reporting a known bug
- *Use a clear descriptive title*
- *Explain what behavior you expected*.
- *Provide a specific example of how to reproduce*. Example code, the
  command(s) you ran, and anything else which may be relevant
- *Include a stacktrace* where applicable

In many cases, you can help by including the following information:

- *What version of python are you running?*
- *What OS and OS version are you running?* ``uname -a`` output helps, but
  additional description like "Ubuntu Linux 17.10" may be useful too
- *What other python packages do you have installed?* The best thing in this
  case is to show us the results of ``pip freeze``

If you are willing and able, *write a failing test*.

Requesting Enhancements
-----------------------

When requesting new features,

- *Say why you want it*. Focus more on the problem which needs to be solved
  than the specifics of how to solve it
- *Suggest what you think is the easiest implementation path*. If you have an
  idea about how a feature could be implemented, write it down
- *Volunteer to write it!* ``nose2`` is maintained as a community effort. If
  you want a new feature, the best way to get it added is to write it
  yourself!


.. _github: https://github.com/
.. _pep8: http://www.python.org/dev/peps/pep-0008/
.. _tox: http://pypi.python.org/pypi/tox
