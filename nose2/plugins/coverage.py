"""
Use this plugin to activate coverage report.

To use this plugin, you need to install ``nose2[coverage_plugin]``. e.g.

::

    $ pip install nose2[coverage_plugin]>=0.6.5


Then, you can enable coverage reporting with :

::

    $ nose2 --with-coverage

Or with this lines in ``unittest.cfg`` :

::

    [coverage]
    always-on = True


You can further specify coverage behaviors with a ``.coveragerc`` file, as
specified by `Coverage Config
<http://coverage.readthedocs.io/en/latest/config.html>`_.
However, when doing so you should also be aware of
`Differences From coverage`_.
"""

import io
import logging

from nose2.events import Plugin

log = logging.getLogger(__name__)


class Coverage(Plugin):
    configSection = "coverage"
    commandLineSwitch = ("C", "with-coverage", "Turn on coverage reporting")
    _mpmode = False
    _subprocess = False

    def __init__(self):
        """Get our config and add our command line arguments."""
        # tracking var for any decision which marks the entire run as failed
        self.decided_failure = False
        # buffer for error output data
        self.error_output_buffer = io.StringIO()

        self.covSource = self.config.as_list("coverage", []) or ["."]
        self.covReport = self.config.as_list("coverage-report", []) or ["term"]
        self.covConfig = (
            self.config.as_str("coverage-config", "").strip() or ".coveragerc"
        )

        group = self.session.pluginargs
        group.add_argument(
            "--coverage",
            action="append",
            default=[],
            metavar="PATH",
            dest="coverage_source",
            help="Measure coverage for filesystem path (multi-allowed)",
        )
        group.add_argument(
            "--coverage-report",
            action="append",
            default=[],
            metavar="TYPE",
            choices=["term", "term-missing", "annotate", "html", "xml"],
            dest="coverage_report",
            help="Generate selected reports, available types:"
            " term, term-missing, annotate, html, xml (multi-allowed)",
        )
        group.add_argument(
            "--coverage-config",
            action="store",
            default="",
            metavar="FILE",
            dest="coverage_config",
            help="Config file for coverage, default: .coveragerc",
        )
        self.covController = None

    def registerInSubprocess(self, event):
        event.pluginClasses.append(self.__class__)
        self._mpmode = True

    def handleArgs(self, event):
        """Get our options in order command line, config file, hard coded."""
        self.covSource = event.args.coverage_source or self.covSource
        self.covReport = event.args.coverage_report or self.covReport
        self.covConfig = event.args.coverage_config or self.covConfig

    def createTests(self, event):
        """Start coverage early to catch imported modules.

        Only called if active so, safe to just start without checking flags"""
        if event.handled:
            log.error(
                "createTests already handled -- "
                "coverage reporting will be inaccurate"
            )
        else:
            log.debug("createTests not already handled. coverage should work")

        self._start_coverage()

    def beforeSummaryReport(self, event):
        """Only called if active so stop coverage and produce reports."""
        if self.covController:
            self.covController.stop()

            # write to .coverage file
            # do this explicitly (instead of passing auto_data=True to
            # Coverage constructor) in order to not load an existing .coverage
            # this better imitates the behavior of invoking `coverage` from the
            # command-line, which sets `Coverage._auto_save` (triggers atexit
            # saving to this file), but not `Coverage._auto_load`
            # requesting a better fix in nedbat/coveragepy#34
            self.covController.save()

            if self._mpmode:
                self.covController.combine(strict=True)

            percent_coverage = None

            if "term" in self.covReport or "term-missing" in self.covReport:
                # only pass `show_missing` if "term-missing" was given
                # otherwise, just allow coverage to load show_missing from
                # config
                kwargs = {}
                if "term-missing" in self.covReport:
                    kwargs["show_missing"] = True
                percent_coverage = self.covController.report(
                    file=self.error_output_buffer, **kwargs
                )
            if "annotate" in self.covReport:
                percent_coverage = self.covController.annotate()
            if "html" in self.covReport:
                percent_coverage = self.covController.html_report()
            if "xml" in self.covReport:
                percent_coverage = self.covController.xml_report()

            fail_under = self.covController.get_option("report:fail_under")
            if (
                fail_under is not None
                and percent_coverage is not None
                and fail_under > percent_coverage
            ):
                self.decided_failure = True

    def startSubprocess(self, event):
        self._mpmode = True
        self._subprocess = True
        self._start_coverage()

    def stopSubprocess(self, event):
        self.covController.stop()
        self.covController.save()

    def wasSuccessful(self, event):
        """Mark full test run as successful or unsuccessful"""
        if self.decided_failure:
            event.success = False

    def afterSummaryReport(self, event):
        """Reporting data is collected, failure status determined and set.
        Now print any buffered error output saved from beforeSummaryReport"""
        print(self.error_output_buffer.getvalue(), file=event.stream)

    def _start_coverage(self):
        try:
            import coverage
        except ImportError:
            print(
                'Warning: you need to install "coverage_plugin" '
                "extra requirements to use this plugin. "
                "e.g. `pip install nose2[coverage_plugin]`"
            )
            return

        self.covController = coverage.Coverage(
            source=self.covSource, config_file=self.covConfig, data_suffix=self._mpmode
        )
        # Call erase() to remove old files. This is important in multiprocess
        # mode, where per-process coverage files are unlikely to be
        # overwritten.
        self.covController.erase()
        # start immediately (don't wait until startTestRun) so that coverage
        # will pick up on things which happen at import time
        self.covController.start()
