import logging
import os
import sys

from nose2.compat import unittest
from nose2 import events, loader, runner, session, util


log = logging.getLogger(__name__)
__unittest = True


class PluggableTestProgram(unittest.TestProgram):
    """TestProgram that enables plugins.

    Accepts the same parameters as :class:`unittest.TestProgram`,
    but most of them are ignored as their functions are
    handled by plugins.

    :param module: Module in which to run tests. Default: __main__
    :param defaultTest: Default test name. Default: None
    :param argv: Command line args. Default: sys.argv
    :param testRunner: *IGNORED*
    :param testLoader: *IGNORED*
    :param exit: Exit after running tests?
    :param verbosity: Base verbosity
    :param failfast: *IGNORED*
    :param catchbreak: *IGNORED*
    :param buffer: *IGNORED*
    :param plugins: List of additional plugin modules to load
    :param excludePlugins: List of plugin modules to exclude

    .. attribute :: sessionClass

       The class to instantiate to create a test run configuration
       session. Default: :class:`nose2.session.Session`

    .. attribute :: loaderClass

       The class to instantiate to create a test loader. Default:
       :class:`nose2.loader.PluggableTestLoader`.

       .. warning ::

          Overriding this attribute is the only way to customize
          the test loader class. Passing a test loader to
          ``__init__`` does not work.

    .. attribute :: runnerClass

       The class to instantiate to create a test runner.  Default:
       :class:`nose2.runner.PluggableTestRunner`.

       .. warning ::

          Overriding this attribute is the only way to customize
          the test runner class. Passing a test runner to
          ``__init__`` does not work.

    .. attribute :: defaultPlugins

       List of default plugin modules to load.

    """
    sessionClass = session.Session
    loaderClass = loader.PluggableTestLoader
    runnerClass = runner.PluggableTestRunner
    defaultPlugins = ('nose2.plugins.loader.discovery',
                      'nose2.plugins.loader.testcases',
                      'nose2.plugins.loader.functions',
                      'nose2.plugins.loader.generators',
                      'nose2.plugins.loader.parameters',
                      'nose2.plugins.result',
                      'nose2.plugins.logcapture',
                      'nose2.plugins.buffer',
                      'nose2.plugins.failfast',
                      'nose2.plugins.debugger',
                      )
    excludePlugins = ()

    # XXX override __init__ to warn that testLoader and testRunner are ignored?
    def __init__(self, **kw):
        plugins = kw.pop('plugins', [])
        exclude = kw.pop('excludePlugins', [])
        self.defaultPlugins = list(self.defaultPlugins)
        self.excludePlugins = list(self.excludePlugins)
        self.defaultPlugins.extend(plugins)
        self.excludePlugins.extend(exclude)
        super(PluggableTestProgram, self).__init__(**kw)

    def parseArgs(self, argv):
        """Parse command line args

        Parses arguments and creates a configuration session,
        then calls createTests.

        """
        self.session = self.sessionClass()
        self.argparse = self.session.argparse # for convenience

        # XXX force these? or can it be avoided?
        self.testLoader = self.loaderClass(self.session)

        # Parse initial arguments like config file paths, verbosity
        self.setInitialArguments()
        # FIXME -h here makes processing stop.
        cfg_args, argv = self.argparse.parse_known_args(argv[1:])
        self.handleCfgArgs(cfg_args)

        # Parse arguments for plugins (if any) and test names
        self.argparse.add_argument('testNames', nargs='*')
        # add help arg now so -h will also print plugin opts
        self.argparse.add_argument('-h', '--help', action='help',
                                   help=('Show this help message and exit'))
        args, argv = self.argparse.parse_known_args(argv)
        if argv:
            self.argparse.error("Unrecognized arguments: %s" % ' '.join(argv))
        self.handleArgs(args)
        self.createTests()

    def setInitialArguments(self):
        """Set pre-plugin command-line arguments.

        This set of arguments is parsed out of the command line
        before plugins are loaded.

        """
        self.argparse.add_argument(
            '-s', '--start-dir', default='.',
            help="Directory to start discovery ('.' default)")
        self.argparse.add_argument(
            '-t', '--top-level-directory', '--project-directory',
            help='Top level directory of project (defaults to start dir)')
        self.argparse.add_argument(
            '--config', '-c', nargs='?', action='append',
            default=['unittest.cfg', 'nose2.cfg'],
            help="Config files to load, if they exist. ('unittest.cfg' "
            "and 'nose2.cfg' in start directory default)")
        self.argparse.add_argument(
            '--no-user-config', action='store_const',
            dest='user_config', const=False, default=True,
            help="Do not load user config files")
        self.argparse.add_argument(
            '--no-plugins', action='store_const',
            dest='load_plugins', const=False, default=True,
            help="Do not load any plugins. Warning: nose2 does not "
            "do anything if no plugins are loaded")
        self.argparse.add_argument(
            '--plugin', action='append',
            dest='plugins', default=[],
            help="Load this plugin module.")
        self.argparse.add_argument(
            '--exclude-plugin', action='append',
            dest='exclude_plugins', default=[],
            help="Do not load this plugin module")
        self.argparse.add_argument('--verbose', '-v', action='count', default=0)
        self.argparse.add_argument('--quiet', action='store_const',
                                 dest='verbose', const=0)
        self.argparse.add_argument(
            '--log-level', default=logging.WARN,
            help='Set logging level for message logged to console.')

    def handleCfgArgs(self, cfg_args):
        """Handle initial arguments.

        Handle the initial, pre-plugin arguments parsed out of the
        command line.

        """
        logging.basicConfig(level=util.parse_log_level(cfg_args.log_level))
        log.debug('logging initialized %s', cfg_args.log_level)
        if cfg_args.verbose:
            self.session.verbosity += cfg_args.verbose
        self.session.startDir = cfg_args.start_dir
        if cfg_args.top_level_directory:
            self.session.topLevelDir = cfg_args.top_level_directory
        self.session.loadConfigFiles(*self.findConfigFiles(cfg_args))
        self.session.prepareSysPath()
        if cfg_args.load_plugins:
            self.defaultPlugins.extend(cfg_args.plugins)
            self.excludePlugins.extend(cfg_args.exclude_plugins)
            self.loadPlugins()
        elif cfg_args.plugins or cfg_args.exclude_plugins:
            log.warn("Both '--no-plugins' and '--plugin' or '--exclude-plugin' "
                     "specified. No plugins were loaded.")

    def findConfigFiles(self, cfg_args):
        """Find available config files"""
        filenames = cfg_args.config[:]
        proj_opts = ('unittest.cfg', 'nose2.cfg')
        for fn in proj_opts:
            if cfg_args.top_level_directory:
                fn = os.path.abspath(
                    os.path.join(cfg_args.top_level_directory, fn))
            filenames.append(fn)
        if cfg_args.user_config:
            user_opts = ('~/.unittest.cfg', '~/.nose2.cfg')
            for fn in user_opts:
                filenames.append(os.path.expanduser(fn))
        return filenames

    def handleArgs(self, args):
        """Handle further arguments.

        Handle arguments parsed out of command line after plugins have
        been loaded (and injected their argument configuration).

        """
        self.testNames = args.testNames
        self.session.hooks.handleArgs(events.CommandLineArgsEvent(args=args))

    def loadPlugins(self):
        """Load available plugins"""
        self.session.loadPlugins(self.defaultPlugins, self.excludePlugins)

    def createTests(self):
        """Create top-level test suite"""
        # XXX belongs in init?
        if self.module and '__unittest' in dir(self.module):
            self.module = None

        event = events.CreateTestsEvent(
           self.testLoader, self.testNames, self.module)
        result = self.session.hooks.createTests(event)
        if event.handled:
           self.test = result
        else:
            log.debug("Create tests from %s/%s", self.testNames, self.module)
            self.test = self.testLoader.loadTestsFromNames(
                self.testNames, self.module)

    def runTests(self):
        """Run tests"""
        # fire plugin hook
        runner = self._makeRunner()
        self.result = runner.run(self.test)
        if self.exit:
            sys.exit(not self.result.wasSuccessful())

    def _makeRunner(self):
        runner = self.runnerClass(self.session)
        event = events.RunnerCreatedEvent(runner)
        self.session.hooks.runnerCreated(event)
        return event.runner


main_ = PluggableTestProgram
