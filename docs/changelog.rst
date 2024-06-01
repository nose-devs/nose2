Changelog
=========

nose2 uses semantic versioning (currently in 0.x) and the popular
"keep a changelog" format (v1.0.0).

nose2 tries not to break backwards compatibility in any release. Until v1.0,
versions are numbered ``0.MAJOR.MINOR``. Major releases introduce new
functionality or contain necessary breaking changes. Minor releases are
primarily used for bugfix or small features which are unlikely to break users'
testsuites.

Unreleased
----------

0.15.1 (2024-05-31)
-------------------

Fixed
~~~~~

* Fix a bug with config loading which caused custom ini configs not to load if
  they were not named with a ``.cfg`` extension. Thanks :user:`grhwalls` for
  the bug report!

0.15.0 (2024-05-30)
-------------------

Added
~~~~~

* Official support for ``python3.13`` betas. ``nose2`` now tests itself against
  Python 3.13.

* ``nose2`` now supports loading configuration data from the ``tool.nose2``
  table in ``pyproject.toml``. Thanks to :user:`qequ` for the PR! (:pr:`596`,
  :pr:`606`)

  On python 3.11+, ``tomllib`` is used to parse TOML data. On python 3.10 and
  lower, ``tomli`` must be installed to enable TOML support. Simply
  ``pip install tomli`` as necessary.

0.14.2 (2024-05-07)
-------------------

Added
~~~~~

* For the coverage plugin, add a config option, ``coverage-combine``, which
  defaults to ``False``. When set, this config invokes a ``coverage combine``
  step before reporting results, regardless of whether or not multiprocessing
  was used to run tests. This allows reporting of coverage results via the
  plugin on testsuites which invoke subprocesses. Thanks to :user:`JCHacking`
  for the PR! (:pr:`601`)

0.14.1 (2024-01-28)
-------------------

Fixed
~~~~~

* Fix the reporting of skipped tests in verbose mode on newer pythons (3.12.1+),
  in which a skipped test is no longer treated as "started".

  ``nose2`` will not introduce a ``StartTestEvent`` in such cases --
  the fix is narrowly and adjustment to the test reporter.

0.14.0 (2023-10-04)
-------------------

Added
~~~~~

* Add official support for ``python3.12``

Removed
~~~~~~~

* Remove support for ``python3.6`` and ``python3.7``

0.13.0 (2023-04-29)
-------------------

Changed
~~~~~~~

* ``nose2`` package metadata is converted to pyproject.toml format, using
  ``setuptools``. Building ``nose2`` packages from source now requires
  ``setuptools>=61.0.0`` or a PEP 517 compatible build frontend
  (e.g. ``build``).

Fixed
~~~~~

* Fix support for python3.12 to avoid warnings about ``addDuration``.
  Thanks to :user:`cclauss` for the fix!

* ``nose2`` license metadata has been corrected in format and content to be
  distributed in the sdist and wheel distributions correctly. Thanks
  :user:`musicinmybrain` for helping research this issue!

Removed
~~~~~~~

* Remove support for python2 and older python3 versions

0.12.0 (2022-07-16)
-------------------

.. note::

   The 0.12.x series will be the final releases of ``nose2`` which support
   Python 2.

Changed
~~~~~~~

* Passing ``--junit-xml-path`` now implies ``--junit-xml`` when using the
  junitxml plugin. This means that the ``--junit-xml`` flag can be omitted
  when ``--junit-xml-path`` is specified. (:issue:`521`)

* Remove the dependency on ``coverage``. Use of the coverage plugin now
  requires that you either install ``coverage`` independently, or use the
  extra, ``nose2[coverage_plugin]``. As a result, ``nose2`` no longer has any
  strict dependencies

* Remove the dependency on ``six``, instead using a vendored copy. This
  ensures that the dependency for ``nose2`` doesn't conflict with application
  dependencies

Removed
~~~~~~~

* ``nose2`` no longer provides an entry-point named based on the current python
  version, e.g. ``nose2-3.8`` on python3.8 . Only the ``nose2`` command is
  provided.

* Remove support for ``setup.py test`` on ``nose2`` itself. This usage is
  deprecated by setuptools. Developers contributing to ``nose2`` are encouraged
  to use ``tox`` to run ``nose2``'s testsuite, per the contributing guide.

0.11.0 (2022-02-12)
-------------------

This is the first version of `nose2` using `sphinx-issues` to credit
contributors in the changelog.

Added
~~~~~

* Test classes now have their short description (first line of docstring)
  printed in verbose output

* The junitxml plugin now sets ``timestamp`` on each ``testcase`` node as an
  ISO-8601 timestamp. Thanks to :user:`deeplow` for the contribution!

Changed
~~~~~~~

* Drop support for Python 3.5

* Python 3.10 is now officially supported. Python 3.11-dev will be supported on
  a best-effort basis. Thanks to :user:`hugovk` and :user:`tirkarthi` for their
  contributions!

* ``nose2`` source code is now autoformatted with ``black`` and ``isort``

* ``nose2`` has switched its main development branch from ``master`` to ``main``

* Releases are now published using `build <https://github.com/pypa/build>`_

Fixed
~~~~~

* Add support for test classes when running with the multiprocessing plugin.
  Thanks to :user:`ltfish` for the initial contribution and
  :user:`stefanholek` for the refinement to this change!

* Various documentation fixes


0.10.0 (2021-01-27)
-------------------

Added
~~~~~

* Support for subtests!

Notes for plugin authors about subtest support:

  * Subtest failures will produce a ``TestOutcomeEvent`` with ``outcome = "subtest"``

  * Subtest events can be failures, but they do not indicate success -- the
    containing test will send a success event if no subtests fail

Changed
~~~~~~~

* Drop support for Python 3.4

* Python 3.8 and 3.9 are now officially supported

* Improve helptext for the multiprocess plugin's ``-N`` option

* When run with reduced verbosity (e.g. with ``-q``), ``nose2`` will no longer
  print an empty line before test reports

Fixed
~~~~~

* The plugin registry will no longer contain duplicate plugins and or base
  ``event.Plugin`` instances

* Fix function test case implementation of ``id``, ``__str__``, and
  ``__repr__``. This removes the injected ``transplant_class.<locals>`` from
  reporting output

* Doctest loading will now skip ``setup.py`` files in the project root

* Class methods decorated (e.g. with ``mock.patch``) are no longer incorrectly
  picked up by the function loader

0.9.2 (2020-02-02)
------------------

Added
~~~~~

* Add ``--junit-xml-path`` to the junit plugin argument list

Fixed
~~~~~

* It is now possible to use the multiprocess and coverage plugins together, as
  long as all of the coverage config is put into the config file

* Minor changes to be compatible with newer pythons (3.8, 3.9)

0.9.1 (2019-04-02)
------------------

Changed
~~~~~~~

* the prof plugin now uses ``cProfile`` instead of ``hotshot`` for profiling, and
  therefore now supports python versions which do not include ``hotshot``

* skipped tests now include the user's reason in junit XML's ``message`` field

Fixed
~~~~~

* the prettyassert plugin mishandled multi-line function definitions

* Using a plugin's CLI flag when the plugin is already enabled via config no
  longer errors -- it is a no-op instead

0.9.0 (2019-03-17)
------------------

Added
~~~~~

* nose2.plugins.prettyassert, enabled with ``--pretty-assert``, which
  pretty-prints AssertionErrors generated by ``assert`` statements

Changed
~~~~~~~

* Update trove classifier to "beta" from "alpha" status

* Cleanup code for EOLed python versions

Removed
~~~~~~~

* Dropped support for ``distutils``. Installation now requires ``setuptools``

Fixed
~~~~~

* Result reporter respects failure status set by other plugins

* JUnit XML plugin now includes the skip reason in its output

0.8.0 (2018-07-31)
------------------

Added
~~~~~

* Add code to enable plugins to documentation

Removed
~~~~~~~

* Dropped support for python 3.3

Fixed
~~~~~

* For junitxml plugin use test module in place of classname if no classname exists

0.7.4 (2018-02-17)
------------------

Added
~~~~~

* Setup tools invocation now handles coverage

Changed
~~~~~~~

* Running ``nose2`` via ``setuptools`` will now trigger ``CreateTestsEvent`` and ``CreatedTestSuiteEvent``

Fixed
~~~~~

* Respect ``fail_under`` in coverage config
* Avoid infinite recursion when loading setuptools from zipped egg
* Manpage now renders reproducibly
* MP doc build now reproducible

0.7.3 (2017-12-13)
------------------

Added
~~~~~

* support for python 3.6.

Fixed
~~~~~

* Tests failing due to .coveragerc not in MANIFEST

0.7.2 (2017-11-14)
------------------

Includes changes from version ``0.7.1``, never released.

Fixed
~~~~~

* Proper indentation of test with docstring in layers
* MP plugin now calls startSubprocess in subprocess

Changed
~~~~~~~

* Add Makefile to enable "quickstart" workflow
* Removed bootstrap.sh and test.sh

Fixed
~~~~~

* Automatically create .coverage file during coverage reporting
* Better handling of import failures

0.7.0 (2017-11-05)
------------------

Note: v0.7.0 drops several unsupported python versions

Added
~~~~~

* Add layer fixture events and hooks
* junit-xml: add logs in "system-out"
* Give full exc_info to loader.failedLoadTests

Changed
~~~~~~~

* Replace cov-core with coverage in the coverage plugin
* Give better error when cannot import a testname
* Better errors when tests fail to load
* Allow combination of MP and OutputBuffer plugins on Python 3

Removed
~~~~~~~

* Dropped unsupported Python 2.6, 3.2, 3.3
* ``nose2.compat`` is removed because it is no longer needed.
  If you have ``from nose2.compat import unittest`` in your code, you will need
  to replace it with ``import unittest``.

Fixed
~~~~~

* Prevent crashing from UnicodeDecodeError
* Fix unicode stream encoding

0.6.5 (2016-06-29)
------------------

Added
~~~~~

* Add `nose2.__version__`

0.6.4 (2016-03-15)
------------------

Fixed
~~~~~

* MP will never spawn more processes than there are tests. e.g. When running
  only one test, only one process is spawned

0.6.3 (2016-03-01)
------------------

Changed
~~~~~~~

* Add support for python 3.4, 3.5

0.6.2 (2016-02-24)
------------------

Fixed
~~~~~

* fix the coverage plugin tests for coverage==3.7.1

0.6.1 (2016-02-23)
------------------

Fixed
~~~~~

* missing test files added to package.

0.6.0 (2016-02-21)
------------------

Added
~~~~~

* Junit XML report support properties
* Add a `createdTestSuite` event, fired after test loading

Changed
~~~~~~~

* Improve test coverage
* Improve CI
* When test loading fails, print the traceback

Fixed
~~~~~

* Junit-xml plugin fixed on windows
* Ensure tests are importable before trying to load them
* Fail test instead of skipping it, when setup fails
* Make the ``collect`` plugin work with layers
* Fix coverage plugin to take import-time coverage into account

0.5.0 (2014-09-14)
------------------

Added
~~~~~

* with_setup and with_teardown decorators to set the setup & teardown
  on a function
* dundertests plugin to skip tests with `__test__ == False`
* `cartesian_params` decorator
* coverage plugin
* EggDiscoveryLoader for discovering tests within Eggs
* Support `params` with `such`
* Include logging output in junit XML

Changed
~~~~~~~

* `such` errors early if Layers plugin is not loaded
* Allow use of `nose2.main()` from within a test module

Fixed
~~~~~

* Such DSL ignores two `such.A` with the same description
* Record skipped tests as 'skipped' instead of 'skips'
* Result output failed on unicode characters
* Fix multiprocessing plugin on Windows
* Ensure plugins write to the event stream
* multiprocessing could lock master proc and fail to exit
* junit report path was sensitive to changes in cwd
* Test runs would crash if a TestCase `__init__` threw an exception
* Plugin failures no longer crash the whole test run
* Handle errors in test setup and teardown
* Fix reporting of xfail tests
* Log capture was waiting too long to render mutable objects to strings
* Layers plugin was not running testSetUp/testTearDown from higher `such` layers

0.4.7 (2013-08-13)
------------------

Added
~~~~~

* start-dir config option. Thanks to Stéphane Klein.
* Help text for verbose flag. Thanks to Tim Sampson.
* Added badges to README. Thanks to Omer Katz.

Changed
~~~~~~~

* Updated six version requirement to be less Restrictive.
  Thanks to Stéphane Klein.
* Cleaned up numerous PEP8 violations. Thanks to Omer Katz.

Fixed
~~~~~

* Fixed broken import in collector.py. Thanks to Shaun Crampton.
* Fixed processes command line option in mp plugin. Thanks to Tim Sampson.
* Fixed handling of class fixtures in multiprocess plugin.
  Thanks to Tim Sampson.
* Fixed intermittent test failure caused by nondeterministic key ordering.
  Thanks to Stéphane Klein.
* Fixed syntax error in printhooks. Thanks to Tim Sampson.
* Fixed formatting in changelog. Thanks to Omer Katz.
* Fixed typos in docs and examples. Thanks to Tim Sampson.

0.4.6 (2013-04-07)
------------------

Changed
~~~~~~~

* Docs note support for python 3.3. Thanks Omer Katz for the bug report.

Fixed
~~~~~

* Fixed DeprecationWarning for compiler package on python 2.7.
  Thanks Max Arnold.
* Fixed lack of timing information in junitxml exception reports. Thanks
  Viacheslav Dukalskiy.
* Cleaned up junitxml xml output. Thanks Philip Thiem.

0.4.5 (2012-12-16)
------------------

Fixed
~~~~~

* Fixed broken interaction between attrib and layers plugins. They can now
  be used together. Thanks @fajpunk.
* Fixed incorrect calling order of layer setup/teardown and test
  setup/test teardown methods. Thanks again @fajpunk for tests and fixes.

0.4.4 (2012-11-26)
------------------

Fixed
~~~~~

* Fixed sort key generation for layers.

0.4.3 (2012-11-21)
------------------

Fixed
~~~~~

* Fixed packaging for non-setuptools, pre-python 2.7. Thanks to fajpunk
  for the patch.

0.4.2 (2012-11-19)
------------------

Added
~~~~~

* Added ``uses`` method to ``such.Scenario`` to allow use of externally-defined
  layers in such DSL tests.

Fixed
~~~~~

* Fixed unpredictable ordering of layer tests.

0.4.1 (2012-06-18)
------------------

Includes changes from version ``0.4``, never released.

Fixed
~~~~~

* Fixed packaging bug.

Added
~~~~~

* nose2.plugins.layers to support Zope testing style fixture layers.
* nose2.tools.such, a spec-like DSL for writing tests with layers.
* nose2.plugins.loader.loadtests to support the unittest2 load_tests protocol.

0.3 (2012-04-15)
----------------

Added
~~~~~

* nose2.plugins.mp to support distributing test runs across multiple processes.
* nose2.plugins.testclasses to support loading tests from ordinary classes that
  are not subclasses of unittest.TestCase.
* ``nose2.main.PluggableTestProgram`` now accepts an ``extraHooks`` keyword
  argument, which allows attaching arbitrary objects to the hooks system.

Changed
~~~~~~~

* The default script target was changed from ``nose2.main`` to ``nose2.discover``.
  The former may still be used for running a single module of tests,
  unittest-style. The latter ignores the ``module`` argument. Thanks to
  @dtcaciuc for the bug report (#32).

Fixed
~~~~~

* Fixed bug that caused Skip reason to always be set to ``None``.

0.2 (2012-02-06)
----------------

Added
~~~~~

* nose2.plugins.junitxml to support jUnit XML output
* nose2.plugins.attrib to support test filtering by attributes

Changed
~~~~~~~

* Added afterTestRun hook and moved result report output calls
  to that hook. This prevents plugin ordering issues with the
  stopTestRun hook (which still exists, and fires before
  afterTestRun).

Fixed
~~~~~

* Fixed bug in loading of tests by name that caused ImportErrors
  to be silently ignored.
* Fixed missing __unittest flag in several modules. Thanks to
  Wouter Overmeire for the patch.
* Fixed module fixture calls for function, generator and param tests.
* Fixed passing of command-line argument values to list
  options. Before this fix, lists of lists would be appended to the
  option target. Now, the option target list is extended with the new
  values. Thanks to memedough for the bug report.

0.1 (2012-01-19)
----------------

Initial release.
