from __future__ import annotations

import logging
import os
import sys
import typing as t
import unittest

from nose2 import events, loader, plugins, runner, session, util
from nose2._toml import TOML_ENABLED

log = logging.getLogger(__name__)
__unittest = True


class PluggableTestProgram(unittest.TestProgram):
    """TestProgram that enables plugins.

    Accepts the same parameters as :class:`unittest.TestProgram`,
    but most of them are ignored as their functions are
    handled by plugins.

    :param module: Module in which to run tests. Default: :func:`__main__`
    :param defaultTest: Default test name. Default: ``None``
    :param argv: Command line args. Default: ``sys.argv``
    :param testRunner: *IGNORED*
    :param testLoader: *IGNORED*
    :param exit: Exit after running tests?
    :param verbosity: Base verbosity
    :param failfast: *IGNORED*
    :param catchbreak: *IGNORED*
    :param buffer: *IGNORED*
    :param plugins: List of additional plugin modules to load
    :param excludePlugins: List of plugin modules to exclude
    :param extraHooks: List of hook names and plugin *instances* to
                       register with the session's hooks system. Each
                       item in the list must be a 2-tuple of
                       (hook name, plugin instance)

    .. attribute :: sessionClass

       The class to instantiate to create a test run configuration
       session. Default: :class:`nose2.session.Session`

    .. attribute :: loaderClass

       The class to instantiate to create a test loader. Default:
       :class:`nose2.loader.PluggableTestLoader`.

       .. warning ::

          Overriding this attribute is the only way to customize
          the test loader class. Passing a test loader to
          :func:`__init__` does not work.

    .. attribute :: runnerClass

       The class to instantiate to create a test runner.  Default:
       :class:`nose2.runner.PluggableTestRunner`.

       .. warning ::

          Overriding this attribute is the only way to customize
          the test runner class. Passing a test runner to
          :func:`__init__` does not work.

    .. attribute :: defaultPlugins

       List of default plugin modules to load.

    """

    sessionClass = session.Session
    _currentSession = None
    loaderClass = loader.PluggableTestLoader
    runnerClass = runner.PluggableTestRunner
    defaultPlugins: t.ClassVar[t.Sequence[str]] = plugins.DEFAULT_PLUGINS
    excludePlugins: t.ClassVar[t.Sequence[str]] = ()

    # XXX override __init__ to warn that testLoader and testRunner are ignored?
    def __init__(self, **kw) -> None:
        plugins = kw.pop("plugins", [])
        exclude = kw.pop("excludePlugins", [])
        hooks = kw.pop("extraHooks", [])
        self.defaultPlugins: list[str] = list(self.defaultPlugins)  # type: ignore[misc]
        self.excludePlugins: list[str] = list(self.excludePlugins)  # type: ignore[misc]
        self.extraHooks = hooks
        self.defaultPlugins.extend(plugins)
        self.excludePlugins.extend(exclude)
        super().__init__(**kw)

    def parseArgs(self, argv):
        """Parse command line args

        Parses arguments and creates a configuration session,
        then calls :func:`createTests`.

        """
        self.session = self.sessionClass()
        self.__class__._currentSession = self.session

        self.argparse = self.session.argparse  # for convenience

        # XXX force these? or can it be avoided?
        self.testLoader = self.loaderClass(self.session)
        self.session.testLoader = self.testLoader

        # Parse initial arguments like config file paths, verbosity
        self.setInitialArguments()
        # FIXME -h here makes processing stop.
        cfg_args, argv = self.argparse.parse_known_args(argv[1:])
        self.handleCfgArgs(cfg_args)

        # Parse arguments for plugins (if any) and test names
        self.argparse.add_argument("testNames", nargs="*")
        # add help arg now so -h will also print plugin opts
        self.argparse.add_argument(
            "-h", "--help", action="help", help="Show this help message and exit"
        )
        args, argv = self.argparse.parse_known_args(argv)
        if argv:
            self.argparse.error("Unrecognized arguments: %s" % " ".join(argv))
        self.handleArgs(args)
        self.createTests()

    def setInitialArguments(self):
        """Set pre-plugin command-line arguments.

        This set of arguments is parsed out of the command line
        before plugins are loaded.

        """
        self.argparse.add_argument(
            "-s",
            "--start-dir",
            default=None,
            help="Directory to start discovery ('.' default)",
        )
        self.argparse.add_argument(
            "-t",
            "--top-level-directory",
            "--project-directory",
            help="Top level directory of project (defaults to start dir)",
        )
        self.argparse.add_argument(
            "--config",
            "-c",
            nargs="?",
            action="append",
            default=["unittest.cfg", "nose2.cfg"],
            help=(
                "Config files to load, if they exist. ('unittest.cfg' "
                "and 'nose2.cfg' in start directory default)"
            ),
        )
        self.argparse.add_argument(
            "--no-user-config",
            action="store_const",
            dest="user_config",
            const=False,
            default=True,
            help="Do not load user config files",
        )
        self.argparse.add_argument(
            "--no-plugins",
            action="store_const",
            dest="load_plugins",
            const=False,
            default=True,
            help=(
                "Do not load any plugins. Warning: nose2 does not "
                "do anything if no plugins are loaded"
            ),
        )
        self.argparse.add_argument(
            "--plugin",
            action="append",
            dest="plugins",
            default=[],
            help="Load this plugin module.",
        )
        self.argparse.add_argument(
            "--exclude-plugin",
            action="append",
            dest="exclude_plugins",
            default=[],
            help="Do not load this plugin module",
        )
        self.argparse.add_argument(
            "--verbosity",
            type=int,
            help="Set starting verbosity level (int). Applies before -v and -q",
        )
        self.argparse.add_argument(
            "--verbose",
            "-v",
            action="count",
            default=0,
            help=(
                "Print test case names and statuses. "
                "Use multiple '-v's for higher verbosity."
            ),
        )
        self.argparse.add_argument(
            "--quiet",
            "-q",
            action="count",
            default=0,
            dest="quiet",
            help="Reduce verbosity. Multiple '-q's result in lower verbosity.",
        )
        self.argparse.add_argument(
            "--log-level",
            default=logging.WARN,
            help="Set logging level for message logged to console.",
        )

    def handleCfgArgs(self, cfg_args):
        """Handle initial arguments.

        Handle the initial, pre-plugin arguments parsed out of the
        command line.

        """
        self.session.logLevel = util.parse_log_level(cfg_args.log_level)
        logging.basicConfig(level=self.session.logLevel)
        log.debug("logging initialized %s", cfg_args.log_level)
        if cfg_args.top_level_directory:
            self.session.topLevelDir = cfg_args.top_level_directory
        self.session.loadConfigFiles(*self.findConfigFiles(cfg_args))
        # set verbosity from config + opts
        self.session.setVerbosity(cfg_args.verbosity, cfg_args.verbose, cfg_args.quiet)
        self.session.setStartDir(args_start_dir=cfg_args.start_dir)
        self.session.prepareSysPath()
        if cfg_args.load_plugins:
            self.defaultPlugins.extend(cfg_args.plugins)
            self.excludePlugins.extend(cfg_args.exclude_plugins)
            self.loadPlugins()
        elif cfg_args.plugins or cfg_args.exclude_plugins:
            log.warn(
                "Both '--no-plugins' and '--plugin' or '--exclude-plugin' "
                "specified. No plugins were loaded."
            )

    def findConfigFiles(self, cfg_args):
        """Find available config files"""
        filenames = cfg_args.config[:]
        proj_opts = ("unittest.cfg", "nose2.cfg")
        if TOML_ENABLED:
            proj_opts += ("pyproject.toml",)
        for fn in proj_opts:
            if cfg_args.top_level_directory:
                fn = os.path.abspath(os.path.join(cfg_args.top_level_directory, fn))
            filenames.append(fn)
        if cfg_args.user_config:
            user_opts = ("~/.unittest.cfg", "~/.nose2.cfg")
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
        """Load available plugins


        :func:`self.defaultPlugins`` and :func:`self.excludePlugins` are passed
        to the session to alter the list of plugins that will be
        loaded.

        This method also registers any (hook, plugin) pairs set in
        ``self.hooks``. This is a good way to inject plugins that fall
        outside of the normal loading procedure, for example, plugins
        that need some runtime information that can't easily be
        passed to them through the configuration system.

        """
        self.session.loadPlugins(self.defaultPlugins, self.excludePlugins)
        for method_name, plugin in self.extraHooks:
            self.session.hooks.register(method_name, plugin)

    def createTests(self):
        """Create top-level test suite"""
        event = events.CreateTestsEvent(self.testLoader, self.testNames, self.module)
        result = self.session.hooks.createTests(event)
        if event.handled:
            test = result
        else:
            log.debug("Create tests from %s/%s", self.testNames, self.module)
            test = self.testLoader.loadTestsFromNames(self.testNames, self.module)

        event = events.CreatedTestSuiteEvent(test)
        result = self.session.hooks.createdTestSuite(event)
        if event.handled:
            test = result
        self.test = test

    def runTests(self):
        """Run tests"""
        # fire plugin hook
        runner = self._makeRunner()
        try:
            self.result = runner.run(self.test)
        except Exception as e:
            log.exception("Internal Error")
            sys.stderr.write("Internal Error: runTests aborted: %s\n" % e)
            if self.exit:
                sys.exit(1)
        if self.exit:
            sys.exit(not self.result.wasSuccessful())

    def _makeRunner(self):
        runner = self.runnerClass(self.session)
        event = events.RunnerCreatedEvent(runner)
        self.session.hooks.runnerCreated(event)
        self.session.testRunner = event.runner
        return event.runner

    @classmethod
    def getCurrentSession(cls):
        """Returns the current session, or ``None`` if no
        :class:`nose2.session.Session` is running.

        """
        return cls._currentSession


main = PluggableTestProgram


def discover(*args, **kwargs):
    """Main entry point for test discovery.

    Running discover calls :class:`nose2.main.PluggableTestProgram`,
    passing through all arguments and keyword arguments **except module**:
    ``module`` is discarded, to force test discovery.

    """
    kwargs["module"] = None
    return main(*args, **kwargs)
