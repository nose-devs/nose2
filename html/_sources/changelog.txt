Changelog
=========

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
