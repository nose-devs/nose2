======================
Tracing hook execution
======================

.. autoplugin :: nose2.plugins.printhooks.PrintHooks

Sample output
-------------

PrintHooks output for a test run that discovers one standard TestCase
test in a python module.

Hooks that appear indented are called from within other hooks.

::

  handleArgs: CommandLineArgsEvent(handled=False, args=Namespace(collect_only=None, config=['unittest.cfg', 'nose2.cfg'], debugger=None, fail_fast=None, load_plugins=True, log_level=30, print_hooks=None, profile=None, start_dir='.', testNames=[], top_level_directory=None, user_config=True, verbose=0, with_id=None))
  
  createTests: CreateTestsEvent(loader=<PluggableTestLoader>, testNames=[], module=<module '__main__' from 'bin/nose2'>)
  
  loadTestsFromNames: LoadFromNames(names=[], module=None)
  
    handleFile: HandleFileEvent(handled=False, loader=<PluggableTestLoader>, name='tests.py', path='nose2/tests/functional/support/scenario/one_test/tests.py', pattern='test*.py', topLevelDirectory='nose2/tests/functional/support/scenario/one_test')
  
    matchPath: MatchPathEvent(handled=False, name='tests.py', path='nose2/tests/functional/support/scenario/one_test/tests.py', pattern='test*.py')
  
    loadTestsFromModule: LoadFromModuleEvent(handled=False, loader=<PluggableTestLoader>, module=<module 'tests' from 'nose2/tests/functional/support/scenario/one_test/tests.py'>, extraTests=[])
  
      loadTestsFromTestCase: LoadFromTestCaseEvent(handled=False, loader=<PluggableTestLoader>, testCase=<class 'tests.Test'>, extraTests=[])
  
      getTestCaseNames: GetTestCaseNamesEvent(handled=False, loader=<PluggableTestLoader>, testCase=<class 'tests.Test'>, testMethodPrefix=None, extraNames=[], excludedNames=[], isTestMethod=<function isTestMethod at 0x1fccc80>)
  
    handleFile: HandleFileEvent(handled=False, loader=<PluggableTestLoader>, name='tests.pyc', path='nose2/tests/functional/support/scenario/one_test/tests.pyc', pattern='test*.py', topLevelDirectory='nose2/tests/functional/support/scenario/one_test')
  
  runnerCreated: RunnerCreatedEvent(handled=False, runner=<PluggableTestRunner>)
  
  resultCreated: ResultCreatedEvent(handled=False, result=<PluggableTestResult>)
  
  startTestRun: StartTestRunEvent(handled=False, runner=<PluggableTestRunner>, suite=<unittest2.suite.TestSuite tests=[<unittest2.suite.TestSuite tests=[<unittest2.suite.TestSuite tests=[<tests.Test testMethod=test>]>]>]>, result=<PluggableTestResult>, startTime=1327346684.77457, executeTests=<function <lambda> at 0x1fccf50>)
  
  startTest: StartTestEvent(handled=False, test=<tests.Test testMethod=test>, result=<PluggableTestResult>, startTime=1327346684.774765)
  
    reportStartTest: ReportTestEvent(handled=False, testEvent=<nose2.events.StartTestEvent object at 0x1fcd650>, stream=<nose2.util._WritelnDecorator object at 0x1f97a10>)
  
  setTestOutcome: TestOutcomeEvent(handled=False, test=<tests.Test testMethod=test>, result=<PluggableTestResult>, outcome='passed', exc_info=None, reason=None, expected=True, shortLabel=None, longLabel=None)
  
  testOutcome: TestOutcomeEvent(handled=False, test=<tests.Test testMethod=test>, result=<PluggableTestResult>, outcome='passed', exc_info=None, reason=None, expected=True, shortLabel=None, longLabel=None)
  
    reportSuccess: ReportTestEvent(handled=False, testEvent=<nose2.events.TestOutcomeEvent object at 0x1fcd650>, stream=<nose2.util._WritelnDecorator object at 0x1f97a10>)
  .
  stopTest: StopTestEvent(handled=False, test=<tests.Test testMethod=test>, result=<PluggableTestResult>, stopTime=1327346684.775064)
  
  stopTestRun: StopTestRunEvent(handled=False, runner=<PluggableTestRunner>, result=<PluggableTestResult>, stopTime=1327346684.77513, timeTaken=0.00056004524230957031)
  
  afterTestRun: StopTestRunEvent(handled=False, runner=<PluggableTestRunner>, result=<PluggableTestResult>, stopTime=1327346684.77513, timeTaken=0.00056004524230957031)
  
  
    beforeErrorList: ReportSummaryEvent(handled=False, stopTestEvent=<nose2.events.StopTestRunEvent object at 0x1eb0d90>, stream=<nose2.util._WritelnDecorator object at 0x1f97a10>, reportCategories={'failures': [], 'skipped': [], 'errors': [], 'unexpectedSuccesses': [], 'expectedFailures': []})
  ----------------------------------------------------------------------
  
    beforeSummaryReport: ReportSummaryEvent(handled=False, stopTestEvent=<nose2.events.StopTestRunEvent object at 0x1eb0d90>, stream=<nose2.util._WritelnDecorator object at 0x1f97a10>, reportCategories={'failures': [], 'skipped': [], 'errors': [], 'unexpectedSuccesses': [], 'expectedFailures': []})
  Ran 1 test in 0.001s
  
  
    wasSuccessful: ResultSuccessEvent(handled=False, result=<PluggableTestResult>, success=False)
  OK
  
    afterSummaryReport: ReportSummaryEvent(handled=False, stopTestEvent=<nose2.events.StopTestRunEvent object at 0x1eb0d90>, stream=<nose2.util._WritelnDecorator object at 0x1f97a10>, reportCategories={'failures': [], 'skipped': [], 'errors': [], 'unexpectedSuccesses': [], 'expectedFailures': []})
