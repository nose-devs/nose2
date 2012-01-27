Hook reference
==============

.. note ::

   Hooks are listed here in order of execution.


Pre-registration Hooks
----------------------

.. function :: pluginsLoaded(self, event)

   :param event: :class:`nose2.events.PluginsLoadedEvent`

   The ``pluginsLoaded`` hook is called after all config files have been read,
   and all plugin classes loaded. Plugins that register automatically
   (those that call :meth:`nose2.events.Plugin.register` in __init__
   or have ``always-on = True`` set in their config file sections) will
   have already been registered with the hooks they implement. Plugins
   waiting for commmand-line activation will not yet be registered.

   Plugins can use this hook to examine or modify the set of loaded plugins,
   inject their own hook methods using
   :meth:`nose2.events.PluginInterface.addMethod`, or take other
   actions to set up or configure themselves or the test run.

   Since ``pluginsLoaded`` is a pre-registration hook, it is called
   for *all plugins* that implement the method, whether they have
   registered or not. Plugins that do not automatically register
   themselves should limit their actions in this hook to
   configuration, since they may not actually be active during the
   test run.

.. function :: handleArgs(self, event)

   :param event: :class:`nose2.events.CommandLineArgsEvent`

   The ``handleArgs`` hook is called after all arguments from the command
   line have been parsed. Plugins can use this hook to handle command-line
   arguments in non-standard ways. They should not use it to try to modify
   arguments seen by other plugins, since the order in which plugins
   execute in a hook is not guaranteed.

   Since ``handleArgs`` is a pre-registration hook, it is called for
   *all plugins* that implement the method, whether they have registered
   or not. Plugins that do not automatically register
   themselves should limit their actions in this hook to
   configuration, since they may not actually be active during the
   test run.


Standard Hooks
--------------

These hooks are called for registered plugins only.


.. function :: createTests(self, event)

   :param event: A :class:`nose2.events.CreateTestsEvent` instance

   Plugins can take over test loading by returning a test suite and setting
   ``event.handled`` to True.

.. function :: loadTestsFromNames(self, event)

   :param event: A :class:`nose2.events.LoadFromNamesEvent` instance

   Plugins can return a test suite or list of test suites and set
   ``event.handled`` to True to prevent other plugins from loading
   tests from the given names, or append tests to
   ``event.extraTests``. Plugins can also remove names from
   ``event.names`` to prevent other plugins from acting on those
   names.

.. function :: loadTestsFromName(self, event)

   :param event: A :class:`nose2.events.LoadFromNameEvent` instance

   Plugins can return a test suite and set ``event.handled`` to True
   to prevent other plugins from loading tests from the given name,
   or append tests to ``event.extraTests``.

.. function :: handleFile(self, event)

   :param event: A :class:`nose2.events.HandleFileEvent` instance

   Plugins can use this hook to load tests from files that are not
   python modules. Plugins may either append tests to ``event.extraTest``,
   or, if they want to prevent other plugins from processing the file,
   set ``event.handled`` to True and return a test case or test suite.

.. function :: matchPath(self, event)

   :param event: A :class:`nose2.events.MatchPathEvent` instance

   Plugins can use this hook to prevent python modules from being
   loaded by the test loader or force them to be loaded by the test
   loader. Set ``event.handled`` to True and return False to cause the
   loader to skip the module. Set ``event.handled`` to True and return
   True to cause the loader to load the module.

.. function :: loadTestsFromModule(self, event)

   :param event: A :class:`nose2.events.LoadFromModuleEvent` instance

   Plugins can use this hook to load tests from test modules. To
   prevent other plugins from loading from the module, set
   ``event.handled`` and return a test suite. Plugins can also append
   tests to ``event.extraTests`` -- ususally that's what you want to
   do, since that will allow other plugins to load their tests from
   the module as well.

.. function :: loadTestsFromTestCase(self, event)

   :param event: A :class:`nose2.events.LoadFromTestCaseEvent` instance

   Plugins can use this hook to load tests from a
   :class:`unittest.TestCase`. To prevent other plugins from loading
   tests from the test case, set ``event.handled`` to True and return
   a test suite. Plugins can also append tests to ``event.extraTests``
   -- ususally that's what you want to do, since that will allow other
   plugins to load their tests from the test case as well.

.. function :: getTestCaseNames(self, event)

   :param event: A :class:`nose2.events.GetTestCaseNamesEvent` instance

   Plugins can use this hook to limit or extend the list of test case
   names that will be loaded from a :class:`unittest.TestCase` by the
   standard nose2 test loader plugins (and other plugins that respect
   the results of the hook). To force a specific list of names, set
   ``event.handled`` to True and return a list: this exact list will
   be the only test case names loaded from the test case. Plugins can
   also extend the list of names by appending test names to
   ``event.extraNames``, and exclude names by appending test names to
   ``event.excludedNames``.

.. function :: runnerCreated(self, event)

   :param event: A :class:`nose2.events.RunnerCreatedEvent` instance

   Plugins can use this hook to wrap, capture or replace the test
   runner. To replace the test runner, set ``event.runner``.

.. function :: resultCreated(self, event)

   :param event: A :class:`nose2.events.ResultCreatedEvent` instance

   Plugins can use this hook to wrap, capture or replace the test
   result. To replace the test result, set ``event.result``.

.. function :: startTestRun(self, event)

   :param event: A :class:`nose2.events.StartTestRunEvent` instance

   Plugins can use this hook to take action before the start of the
   test run, and to replace or wrap the test executor. To replace the
   executor, set ``event.executeTests``. This must be a callable that
   takes two arguments: the top-level test and the test result.

   To prevent the test executor from running at all, set
   ``event.handled`` to True.

.. function :: startTest(self, event)

   :param event: A :class:`nose2.events.StartTestEvent` instance

   Plugins can use this hook to take action immediately before a test
   runs.

.. function :: reportStartTest(self, event)

   :param event: A :class:`nose2.events.ReportTestEvent` instance

   Plugins can use this hook to produce output for the user at the
   start of a test. If you want to print to the console, write to
   ``event.stream``. Remember to respect self.session.verbosity when
   printing to the console. To prevent other plugins from reporting
   to the user, set ``event.handled`` to True.

.. function :: describeTest(self, event)

   :param event: A :class:`nose2.events.DescribeTestEvent` instance

   Plugins can use this hook to alter test descriptions. To return a
   nonstandard description for a test, set ``event.description``. Be
   aware that other plugins may have set this also!

.. function :: setTestOutcome(self, event)

   :param event: A :class:`nose2.events.TestOutcomeEvent` instance

   Plugins can use this hook to alter test outcomes. Plugins can
   ``event.outcome`` to change the outcome of the event, tweak, change
   or remove ``event.exc_info``, set or clear ``event.expected``, and
   so on.

.. function :: testOutcome(self, event)

   :param event: A :class:`nose2.events.TestOutcomeEvent` instance

   Plugins can use this hook to take action based on the outcome of
   tests. Plugins *must not* alter test outcomes in this hook: that's
   what :func:`setTestOutcome` is for. Here, plugins may only react to
   the outcome event, not alter it.

.. function :: reportSuccess(self, event)

   :param event: A :class:`nose2.events.LoadFromNamesEvent` instance

   Plugins can use this hook to report test success to the user. If
   you want to print to the console, write to
   ``event.stream``. Remember to respect self.session.verbosity when
   printing to the console. To prevent other plugins from reporting to
   the user, set ``event.handled`` to True.

.. function :: reportError(self, event)

   :param event: A :class:`nose2.events.ReportTestEvent` instance

   Plugins can use this hook to report a test error to the user. If
   you want to print to the console, write to
   ``event.stream``. Remember to respect self.session.verbosity when
   printing to the console. To prevent other plugins from reporting to
   the user, set ``event.handled`` to True.

.. function :: reportFailure(self, event)

   :param event: A :class:`nose2.events.ReportTestEvent` instance

   Plugins can use this hook to report test failure to the user. If
   you want to print to the console, write to
   ``event.stream``. Remember to respect self.session.verbosity when
   printing to the console. To prevent other plugins from reporting to
   the user, set ``event.handled`` to True.

.. function :: reportSkip(self, event)

   :param event: A :class:`nose2.events.ReportTestEvent` instance

   Plugins can use this hook to report a skipped test to the user. If
   you want to print to the console, write to
   ``event.stream``. Remember to respect self.session.verbosity when
   printing to the console. To prevent other plugins from reporting to
   the user, set ``event.handled`` to True.

.. function :: reportExpectedFailure(self, event)

   :param event: A :class:`nose2.events.ReportTestEvent` instance

   Plugins can use this hook to report an expected failure to the
   user. If you want to print to the console, write to
   ``event.stream``. Remember to respect self.session.verbosity when
   printing to the console. To prevent other plugins from reporting to
   the user, set ``event.handled`` to True.

.. function :: reportUnexpectedSuccess(self, event)

   :param event: A :class:`nose2.events.ReportTestEvent` instance

   Plugins can use this hook to report an unexpected success to the
   user. If you want to print to the console, write to
   ``event.stream``. Remember to respect self.session.verbosity when
   printing to the console. To prevent other plugins from reporting to
   the user, set ``event.handled`` to True.

.. function :: reportOtherOutcome(self, event)

   :param event: A :class:`nose2.events.ReportTestEvent` instance

   Plugins can use this hook to report a custom test outcome to the
   user. If you want to print to the console, write to
   ``event.stream``. Remember to respect self.session.verbosity when
   printing to the console. To prevent other plugins from reporting to
   the user, set ``event.handled`` to True.

.. function :: stopTest(self, event)

   :param event: A :class:`nose2.events.StopTestEvent` instance

   Plugins can use this hook to take action after a test has completed
   running and reported its outcome.

.. function :: stopTestRun(self, event)

   :param event: A :class:`nose2.events.StopTestRunEvent` instance

   Plugins can use this hook to take action at the end of a test run.

.. function :: afterTestRun(self, event)

   :param event: A :class:`nose2.events.StopTestRunEvent` instance

   Plugins can use this hook to take action *after* the end of a test
   run, such as printing summary reports like the builtin result
   reporter plugin :class:`nose2.plugins.result.ResultReporter`.

.. function :: resultStop(self, event)

   :param event: A :class:`nose2.events.ResultStopEvent` instance

   Plugins can use this hook to *prevent* other plugins from stopping
   a test run. This hook fires when something calls
   :meth:`nose2.result.PluggableTestResult.stop`. If you want to
   prevent this from stopping the test run, set ``event.shouldStop``
   to False.

.. function :: beforeErrorList(self, event)

   :param event: A :class:`nose2.events.ReportSummaryEvent` instance

   Plugins can use this hook to output or modify summary information
   before the list of errors and failures is output. To modify the
   categories of outcomes that will be reported, plugins can modify
   the ``event.reportCategories`` dictionary. Plugins can set, wrap or
   capture the output stream by reading or setting ``event.stream``.
   If you want to print to the console, write to
   ``event.stream``. Remember to respect self.session.verbosity when
   printing to the console.

.. function :: outcomeDetail(self, event)

   :param event: A :class:`nose2.events.OutcomeDetailEvent` instance

   Plugins can use this hook to add additional elements to error list
   output. Append extra detail lines to ``event.extraDetail``; these
   will be joined together with newlines before being output as part
   of the detailed error/failure message, after the traceback.

.. function :: beforeSummaryReport(self, event)

   :param event: A :class:`nose2.events.ReportSummaryEvent` instance

   Plugins can use this hook to output or modify summary information
   before the summary lines are output.  To modify the categories of
   outcomes that will be reported in the summary, plugins can modify
   the ``event.reportCategories`` dictionary. Plugins can set, wrap or
   capture the output stream by reading or setting
   ``event.stream``. If you want to print to the console, write to
   ``event.stream``. Remember to respect self.session.verbosity when
   printing to the console.

.. function :: wasSuccessful(self, event)

   :param event: A :class:`nose2.events.ResultSuccessEvent` instance

   Plugins can use this hook to mark a test run as successful or
   unsuccessful. If not plugin marks the run as successful, the
   default state is failure. To mark a run as successful, set
   ``event.success`` to True. Be ware that other plugins may set this
   attribute as well!

.. function :: afterSummaryReport(self, event)

   :param event: A :class:`nose2.events.ReportSummaryEvent` instance

   Plugins can use this hook to output a report to the user after the
   summary line is output. If you want to print to the console, write
   to ``event.stream``. Remember to respect self.session.verbosity
   when printing to the console.


User Interaction Hooks
----------------------

These hooks are called when plugins want to interact with the user.

.. function :: beforeInteraction(event)

   :param event: A :class:`nose2.events.UserInteractionEvent`

   Plugins should respond to this hook by getting out of the way of
   user interaction, if the need to, or setting ``event.handled`` and
   returning False, if they need to but can't.


.. function :: afterInteraction(event)

   :param event: A :class:`nose2.events.UserInteractionEvent`

   Plugins can respond to this hook by going back to whatever they
   were doing before the user stepped in and started poking around.
