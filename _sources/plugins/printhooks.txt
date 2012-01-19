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

  handleArgs: CommandLineArgsEvent(handled=False, args=Namespace(collect_only=None, config=['unittest.cfg', 'nose2.cfg'], debugger=None, fail_fast=None, load_plugins=True, log_capture=None, output_buffer=None, print_hooks=None, start_dir='.', testNames=[], top_level_directory=None, user_config=True, verbose=0))
  
  createTests: CreateTestsEvent(loader=<nose2.loader.PluggableTestLoader object at 0x1843210>, testNames=[], module=<module '__main__' from '/home/jpellerin/code/nose2-gh/nose2/__main__.py'>)
  
  loadTestsFromNames: LoadFromNames(names=[], module=None)
  
    handleFile: HandleFileEvent(handled=False, loader=<nose2.loader.PluggableTestLoader object at 0x1843210>, name='tests.py', path='/home/jpellerin/code/nose2-gh/nose2/tests/functional/support/scenario/one_test/tests.py', pattern='test*.py', topLevelDirectory='/home/jpellerin/code/nose2-gh/nose2/tests/functional/support/scenario/one_test')
  
    matchPath: MatchPathEvent(handled=False, name='tests.py', path='/home/jpellerin/code/nose2-gh/nose2/tests/functional/support/scenario/one_test/tests.py', pattern='test*.py')
  
    loadTestsFromModule: LoadFromModuleEvent(handled=False, loader=<nose2.loader.PluggableTestLoader object at 0x1843210>, module=<module 'tests' from '/home/jpellerin/code/nose2-gh/nose2/tests/functional/support/scenario/one_test/tests.pyc'>, extraTests=[])
  
      loadTestsFromTestCase: LoadFromTestCaseEvent(handled=False, loader=<nose2.loader.PluggableTestLoader object at 0x1843210>, testCase=<class 'tests.Test'>, extraTests=[])
  
      getTestCaseNames: GetTestCaseNamesEvent(handled=False, loader=<nose2.loader.PluggableTestLoader object at 0x1843210>, testCase=<class 'tests.Test'>, testMethodPrefix=None, extraNames=[], excludedNames=[], isTestMethod=<function isTestMethod at 0x18fb668>)
  
    handleFile: HandleFileEvent(handled=False, loader=<nose2.loader.PluggableTestLoader object at 0x1843210>, name='tests.pyc', path='/home/jpellerin/code/nose2-gh/nose2/tests/functional/support/scenario/one_test/tests.pyc', pattern='test*.py', topLevelDirectory='/home/jpellerin/code/nose2-gh/nose2/tests/functional/support/scenario/one_test')
  
  runnerCreated: RunnerCreatedEvent(handled=False, runner=<nose2.runner.PluggableTestRunner object at 0x1843450>)
  
  resultCreated: ResultCreatedEvent(handled=False, result=<nose2.result.PluggableTestResult object at 0x1847850>)
  
  startTestRun: StartTestRunEvent(handled=False, runner=<nose2.runner.PluggableTestRunner object at 0x1843450>, suite=<unittest2.suite.TestSuite tests=[<unittest2.suite.TestSuite tests=[<unittest2.suite.TestSuite tests=[<tests.Test testMethod=test>]>]>]>, result=<nose2.result.PluggableTestResult object at 0x1847850>, startTime=1326751525.980829, executeTests=<function <lambda> at 0x18fbaa0>)
  
  startTest: StartTestEvent(handled=False, test=<tests.Test testMethod=test>, result=<nose2.result.PluggableTestResult object at 0x1847850>, startTime=1326751525.9809561)
  
    reportStartTest: ReportTestEvent(handled=False, testEvent=<nose2.events.StartTestEvent object at 0x1934690>, stream=<nose2.util._WritelnDecorator object at 0x18f4990>)
  
    describeTest: DescribeTestEvent(handled=False, test=<tests.Test testMethod=test>, description=None)
  test (tests.Test) ... 
  testOutcome: TestOutcomeEvent(handled=False, test=<tests.Test testMethod=test>, result=<nose2.result.PluggableTestResult object at 0x1847850>, outcome='passed', exc_info=None, reason=None, expected=True, shortLabel=None, longLabel=None)
  
    setTestOutcome: TestOutcomeEvent(handled=False, test=<tests.Test testMethod=test>, result=<nose2.result.PluggableTestResult object at 0x1847850>, outcome='passed', exc_info=None, reason=None, expected=True, shortLabel=None, longLabel=None)
  
    reportSuccess: ReportTestEvent(handled=False, testEvent=<nose2.events.TestOutcomeEvent object at 0x1934690>, stream=<nose2.util._WritelnDecorator object at 0x18f4990>)
  ok
  
  stopTest: StopTestEvent(handled=False, test=<tests.Test testMethod=test>, result=<nose2.result.PluggableTestResult object at 0x1847850>, stopTime=1326751525.9812191)
  
  stopTestRun: StopTestRunEvent(handled=False, runner=<nose2.runner.PluggableTestRunner object at 0x1843450>, result=<nose2.result.PluggableTestResult object at 0x1847850>, stopTime=1326751525.9812679, timeTaken=0.00043892860412597656)
  
  
    beforeErrorList: ReportSummaryEvent(handled=False, stopTestEvent=<nose2.events.StopTestRunEvent object at 0x18f4b10>, stream=<nose2.util._WritelnDecorator object at 0x18f4990>, reportCategories={'failures': [], 'skipped': [], 'errors': [], 'unexpectedSuccesses': [], 'expectedFailures': []})
  ----------------------------------------------------------------------
  
    beforeSummaryReport: ReportSummaryEvent(handled=False, stopTestEvent=<nose2.events.StopTestRunEvent object at 0x18f4b10>, stream=<nose2.util._WritelnDecorator object at 0x18f4990>, reportCategories={'failures': [], 'skipped': [], 'errors': [], 'unexpectedSuccesses': [], 'expectedFailures': []})
  Ran 1 test in 0.000s
  
  
    wasSuccessful: ResultSuccessEvent(handled=False, result=<nose2.result.PluggableTestResult object at 0x1847850>, success=False)
  OK
  
    afterSummaryReport: ReportSummaryEvent(handled=False, stopTestEvent=<nose2.events.StopTestRunEvent object at 0x18f4b10>, stream=<nose2.util._WritelnDecorator object at 0x18f4990>, reportCategories={'failures': [], 'skipped': [], 'errors': [], 'unexpectedSuccesses': [], 'expectedFailures': []})
