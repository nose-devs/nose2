Changelog
=========

0.7.4
----------

* Fixed
    * Respect `fail_under` in converage config
    * Avoid infinite recursion when loading setuptools from zipped egg
    * Manpage now renders reproducably
    * MP doc build now reproducable
  
* Features 
    * Setup tools invocation now handles coverage

* Notes
    * Running `nose2` via `setuptools` will now trigger `CreateTestsEvent` and `CreatedTestSuiteEvent`

0.7.3
-----

* Fixed
    * Tests failing due to .coveragerc not in MANIFEST

Added support for python 3.6.

0.7.2
-----

* Fixed
    * Proper indentation of test with docstring in layers 
    * MP plugin now calls startSubprocess in subprocess

0.7.1
-----
(Built but never deployed.)

* Fixed
    * Automatically create .coverage file during coverage reporting
    * Better handling of import failures

* Developer workflow changes
    * Add Makefile to enable "quickstart" workflow
    * Removed bootstrap.sh and test.sh

0.7.0
-----

* BREAKING Dropped unsupported Python 2.6, 3.2, 3.3
    * Added support for Python 3.4, 3.5
    * ``nose2.compat`` is removed because it is no longer needed. If you have ``from nose2.compat import unittest`` in your code, you will need to replace it with ``import unittest``.

* Replace cov-core with coverage plugin

* Fixed
    * Prevent crashing from UnicodeDecodeError
    * Fix unicode stream encoding

* Features
    * Add layer fixture events and hooks
    * junit-xml: add logs in "system-out"
    * Give better error when cannot import a testname
    * Give full exc_info to loader.failedLoadTests
    * Better errors when tests fail to load
    * Reduce the processes created in the MP plugin if there are not enough tests.
    * Allow combination of MP and OutputBuffer plugins on Python 3

0.6.2
-----

* Fixed
    * fix the coverage plugin tests for coverage==3.7.1

0.6.1
-----

* Fixed
    * missing test files added to package.

0.6.0
-----

* Added
    * Junit XML report support properties
    * Improve test coverage
    * Improve CI
    * Add a `createdTestSuite` event, fired after test loading

* Fixed
    * Junit-xml plugin fixed on windows
    * Ensure tests are importable before trying to load them
    * Fail test instead of skipping it, when setup fails
    * When test loading fails, print the traceback
    * Make the ``collect`` plugin work with layers
    * Fix coverage plugin to take import-time coverage into account

0.4.7
-----

* Feature: Added start-dir config option. Thanks to Stéphane Klein.

* Bug: Fixed broken import in collector.py. Thanks to Shaun Crampton.

* Bug: Fixed processes command line option in mp plugin. Thanks to Tim Sampson.

* Bug: Fixed handling of class fixtures in multiprocess plugin.
  Thanks to Tim Sampson.

* Bug: Fixed intermittent test failure caused by nondeterministic key ordering.
  Thanks to Stéphane Klein.

* Bug: Fixed syntax error in printhooks. Thanks to Tim Sampson.

* Docs: Fixed formatting in changelog. Thanks to Omer Katz.

* Docs: Added help text for verbose flag. Thanks to Tim Sampson.

* Docs: Fixed typos in docs and examples. Thanks to Tim Sampson.

* Docs: Added badges to README. Thanks to Omer Katz.

* Updated six version requirement to be less Restrictive.
  Thanks to Stéphane Klein.

* Cleaned up numerous PEP8 violations. Thanks to Omer Katz.

0.4.6
-----

* Bug: fixed DeprecationWarning for compiler package on python 2.7.
  Thanks Max Arnold.

* Bug: fixed lack of timing information in junitxml exception reports. Thanks
  Viacheslav Dukalskiy.

* Bug: cleaned up junitxml xml output. Thanks Philip Thiem.

* Docs: noted support for python 3.3. Thanks Omer Katz for the bug report.

0.4.5
-----

* Bug: fixed broken interaction between attrib and layers plugins. They can now
  be used together. Thanks @fajpunk.

* Bug: fixed incorrect calling order of layer setup/teardown and test
  setup/test teardown methods. Thanks again @fajpunk for tests and fixes.

0.4.4
-----

* Bug: fixed sort key generation for layers.

0.4.3
-----

* Bug: fixed packaging for non-setuptools, pre-python 2.7. Thanks to fajpunk
  for the patch.

0.4.2
-----

* Bug: fixed unpredictable ordering of layer tests.

* Added ``uses`` method to ``such.Scenario`` to allow use of externally-defined
  layers in such DSL tests.

0.4.1
-----

* Fixed packaging bug.

0.4
---

* New plugin: Added nose2.plugins.layers to support Zope testing style
  fixture layers.

* New tool: Added nose2.tools.such, a spec-like DSL for writing tests
  with layers.

* New plugin: Added nose2.plugins.loader.loadtests to support the
  unittest2 load_tests protocol.

0.3
---

* New plugin: Added nose2.plugins.mp to support distributing test runs
  across multiple processes.

* New plugin: Added nose2.plugins.testclasses to support loading tests
  from ordinary classes that are not subclasses of unittest.TestCase.

* The default script target was changed from ``nose2.main`` to ``nose2.discover``.
  The former may still be used for running a single module of tests,
  unittest-style. The latter ignores the ``module`` argument. Thanks to
  @dtcaciuc for the bug report (#32).

* ``nose2.main.PluggableTestProgram`` now accepts an ``extraHooks`` keyword
  argument, which allows attaching arbitrary objects to the hooks system.

* Bug: Fixed bug that caused Skip reason to always be set to ``None``.

0.2
---

* New plugin: Added nose2.plugins.junitxml to support jUnit XML output.

* New plugin: Added nose2.plugins.attrib to support test filtering by
  attributes.

* New hook: Added afterTestRun hook, moved result report output calls
  to that hook. This prevents plugin ordering issues with the
  stopTestRun hook (which still exists, and fires before
  afterTestRun).

* Bug: Fixed bug in loading of tests by name that caused ImportErrors
  to be silently ignored.

* Bug: Fixed missing __unittest flag in several modules. Thanks to
  Wouter Overmeire for the patch.

* Bug: Fixed module fixture calls for function, generator and param tests.

* Bug: Fixed passing of command-line argument values to list
  options. Before this fix, lists of lists would be appended to the
  option target. Now, the option target list is extended with the new
  values. Thanks to memedough for the bug report.

0.1
---

Initial release.
