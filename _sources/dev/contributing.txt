Contributing to nose2
=====================

Exhortation
-----------

Please do! nose2 cannot move forward without contributions from the
testing community.

The Basics
----------

nose2 is hosted on `github`_. Our home there is
https://github.com/nose-devs/nose2. We use github's issue tracking and
collaboration tools *exclusively* for managing nose2's
development. This means:

* Please report issues here: https://github.com/nose-devs/nose2/issues

* Please make feature requests in the same place.

* Please submit all patches as github pull requests.

Coding Guidelines
-----------------

Our style is `pep8`_ except: for consistency with unittest, please use CamelCase
for class names, methods, attributes and function parameters that map
directly to class attributes.

Beyond style, the main rule is: *any patch that touches code must
include tests.* And of course all tests must pass under all supported
versions of Python.

Fortunately that's easy to check: nose2 uses `tox`_ to manage its test
scenarios, so simply running ``tox`` in nose2's root directory will
run all of the tests with all supported python versions. When your
patch gets all green, send a pull request!

Merging Guidelines
------------------

The github Merge Button(tm) should be used only for trivial
changes. Other merges, even those that can be automatically merged,
should be merged manually, so that you have an opportunity to run
tests on the merged changes before pushing them. When you merge
manually, please use ``--no-ff`` so that we have a record of all
merges.

Also, core devs should not merge their own work -- again, unless it's
trivial -- without giving other developers a chance to review it. The
basic worfklow should be to do the work in a topic branch in your fork
then post a pull request for that branch, whether you're a core
developer or other contributor.


.. _github: https://github.com/
.. _pep8: http://www.python.org/dev/peps/pep-0008/
.. _tox: http://pypi.python.org/pypi/tox
