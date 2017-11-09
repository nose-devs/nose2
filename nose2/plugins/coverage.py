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

"""
from __future__ import absolute_import
import logging

from nose2.events import Plugin

log = logging.getLogger(__name__)


class Coverage(Plugin):
    configSection = 'coverage'
    commandLineSwitch = ('C', 'with-coverage', 'Turn on coverage reporting')

    def __init__(self):
        """Get our config and add our command line arguments."""
        self.conSource = self.config.as_list('coverage', [])
        self.conReport = self.config.as_list('coverage-report', [])
        self.conConfig = self.config.as_str('coverage-config', '').strip()

        group = self.session.pluginargs
        group.add_argument(
            '--coverage', action='append', default=[], metavar='PATH',
            dest='coverage_source',
            help='Measure coverage for filesystem path (multi-allowed)'
        )
        group.add_argument(
            '--coverage-report', action='append', default=[], metavar='TYPE',
            choices=['term', 'term-missing', 'annotate', 'html', 'xml'],
            dest='coverage_report',
            help='Generate selected reports, available types:'
                 ' term, term-missing, annotate, html, xml (multi-allowed)'
        )
        group.add_argument(
            '--coverage-config', action='store', default='', metavar='FILE',
            dest='coverage_config',
            help='Config file for coverage, default: .coveragerc'
        )
        self.covController = None

    def handleArgs(self, event):
        """Get our options in order command line, config file, hard coded."""

        self.covSource = (event.args.coverage_source or
                          self.conSource or ['.'])
        self.covReport = (event.args.coverage_report or
                          self.conReport or ['term'])
        self.covConfig = (event.args.coverage_config or
                          self.conConfig or '.coveragerc')

    def createTests(self, event):
        """Start coverage early to catch imported modules.

        Only called if active so, safe to just start without checking flags"""
        try:
            import coverage
        except ImportError:
            print('Warning: you need to install "coverage_plugin" '
                  'extra requirements to use this plugin. '
                  'e.g. `pip install nose2[coverage_plugin]`')
            return

        if event.handled:
            log.error(
                'createTests already handled -- '
                'coverage reporting will be inaccurate')
        else:
            log.debug(
                'createTests not already handled. coverage should work')

        self.covController = coverage.Coverage(source=self.covSource,
                                               config_file=self.covConfig)
        # start immediately (don't wait until startTestRun) so that coverage
        # will pick up on things which happen at import time
        self.covController.start()

    def afterSummaryReport(self, event):
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

            if 'term' in self.covReport or 'term-missing' in self.covReport:
                # only pass `show_missing` if "term-missing" was given
                # otherwise, just allow coverage to load show_missing from
                # config
                kwargs = {}
                if 'term-missing' in self.covReport:
                    kwargs['show_missing'] = True
                self.covController.report(file=event.stream, **kwargs)
            if 'annotate' in self.covReport:
                self.covController.annotate()
            if 'html' in self.covReport:
                self.covController.html_report()
            if 'xml' in self.covReport:
                self.covController.xml_report()
