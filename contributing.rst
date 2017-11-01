Contributing to nose2
=====================

First off, thank you so much for taking the time to contribute! :+1:

This document is a set of guidelines, not strict rules.
Use your best judgement, and feel free to propose changes to this document
in a pull request.


Reporting Bugs
--------------

We welcome any and all bugs on the
`GitHub Issue Tracker <https://github.com/nose-devs/nose2/issues>`_.

However, the best bug reports are ones which:

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

Code Contributions
------------------

Commit Messages
~~~~~~~~~~~~~~~

A few basic ground rules for what ideal commits should look like.

- No lines over 72 characters
- No GitHub emoji -- use your words
- Reference issues and pull requests where appropriate
- Present tense and imperative mood

Style Guide
~~~~~~~~~~~

Some tips for the python and documentation in this project.

- Code should pass ``flake8``. That means PEP8 compliant and passing ``pyflakes``
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

Submitting Pull Requests
~~~~~~~~~~~~~~~~~~~~~~~~

- *Make sure it meets the standards set in this document*
- *Make sure it merges cleanly*
- *List any issues closed by the pull request*
- *Squash intermediate commits*. Use ``git rebase --interactive`` to squash
  typo fixes, aborted implementations, etc.
