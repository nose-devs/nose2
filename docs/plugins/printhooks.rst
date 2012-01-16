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

  handleArgs: <CommandLineArgsEvent>
  createTests: <CreateTestsEvent>
  loadTestsFromNames: LoadFromNames(names=[], module=None)
    handleFile: <HandleFileEvent>
    matchPath: <MatchPathEvent>
    loadTestsFromModule: <LoadFromModuleEvent>
      loadTestsFromTestCase: <LoadFromTestCaseEvent>
      getTestCaseNames: <GetTestCaseNamesEvent>
    handleFile: <HandleFileEvent>
  runnerCreated: <RunnerCreatedEvent>
  resultCreated: <ResultCreatedEvent>
  startTestRun: <StartTestRunEvent>
  startTest: <StartTestEvent>
    reportStartTest: <ReportTestEvent>
  testOutcome: <TestOutcomeEvent>
    setTestOutcome: <TestOutcomeEvent>
    reportSuccess: <ReportTestEvent>
  .stopTest: <StopTestEvent>
  stopTestRun: <StopTestRunEvent>

    beforeErrorList: <ReportSummaryEvent>
  ----------------------------------------------------------------------
    beforeSummaryReport: <ReportSummaryEvent>
  Ran 1 test in 0.000s

    wasSuccessful: <ResultSuccessEvent>
  OK
    afterSummaryReport: <ReportSummaryEvent>
