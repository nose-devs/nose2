Contributing to nose2
=====================

Please do! nose2 cannot move forward without contributions from the
testing community.

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

The main rule is: *any patch that touches code must include tests.*
And of course all tests must pass under all supported versions of Python.

Fortunately that's easy to check: nose2 uses `tox`_ to manage its test
scenarios, so simply running ``tox`` in nose2's root directory will
run all of the tests with all supported python versions. When your
patch gets all green, send a pull request!

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
- Present tense and imperative mood

Workflow and Merging
--------------------

Get Started
~~~~~~~~~~~

The ``bootstrap.sh`` script in the root of the nose2 distribution can be
used to get a new local clone up and running quickly. It requires that
you have `virtualenvwrapper`_ installed. Run this script once to set
up a nose2 virtualenv, install nose2's dependencies, and set up the
git submodule that pulls in the `Sphinx`_ theme that the docs use.

Branching and Pull Requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The basic workflow should be to do the work in a topic branch in your fork
then post a pull request for that branch.

Core devs should not merge their own work -- unless it's trivial -- without
giving other developers a chance to review it.

For any pull request,

- *Make sure it meets the standards set in this document*
- *Make sure it merges cleanly*
- *List any issues closed by the pull request*
- *Squash intermediate commits*. Use ``git rebase --interactive`` to squash
  typo fixes, aborted implementations, etc.

Merging
~~~~~~~

When merging via GitHub, please elect to create a merge commit (the default).
When you merge manually, please use ``--no-ff``.

This ensures that we have a record of all merges in the form of merge commits.

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
.. _virtualenvwrapper: http://pypi.python.org/pypi/virtualenvwrapper
.. _Sphinx: http://sphinx.pocoo.org/
