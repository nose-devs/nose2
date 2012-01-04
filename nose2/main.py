import logging
import os
import sys

from nose2.compat import unittest
from nose2 import events, loader, runner, session


log = logging.getLogger(__name__)
__unittest = True


class PluggableTestProgram(unittest.TestProgram):
    sessionClass = session.Session
    loaderClass = loader.PluggableTestLoader
    runnerClass = runner.PluggableTestRunner
    defaultPlugins = ['nose2.plugins.loader.discovery',
                      'nose2.plugins.loader.testcases',
                      'nose2.plugins.loader.functions',
                      'nose2.plugins.loader.generators',
                      'nose2.plugins.loader.parameters',
                      'nose2.plugins.result',
                      'nose2.plugins.collect',
                      'nose2.plugins.logcapture',
                      # etc
                      ]
    # XXX override __init__ to warn that testLoader and testRunner are ignored?

    def parseArgs(self, argv):
        log.debug("parse argv %s", argv)
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
        args, argv = self.argparse.parse_known_args(argv)
        if argv:
            self.argparse.error("Unrecognized arguments: %s" % ' '.join(argv))
        self.handleArgs(args)
        self.createTests()

    def setInitialArguments(self):
        self.argparse.add_argument(
            '-s', '--start-dir', default='.',
            help="Directory to start discovery ('.' default)")
        self.argparse.add_argument(
            '-t', '--top-level-directory', '--project-directory',
            help='Top level directory of project (defaults to start dir)')
        self.argparse.add_argument('--config', '-c', nargs='?', action='append',
                                 default=['unittest.cfg', 'nose2.cfg'])
        self.argparse.add_argument('--no-user-config', action='store_const',
                                 dest='user_config', const=False, default=True)
        self.argparse.add_argument('--no-plugins', action='store_const',
                                 dest='load_plugins', const=False, default=True)
        self.argparse.add_argument('--verbose', '-v', action='count', default=0)
        self.argparse.add_argument('--quiet', action='store_const',
                                 dest='verbose', const=0)

    def handleCfgArgs(self, cfg_args):
        if cfg_args.verbose:
            self.session.verbosity += cfg_args.verbose
        self.session.startDir = cfg_args.start_dir
        if cfg_args.top_level_directory:
            self.session.topLevelDir = cfg_args.top_level_directory
        self.session.loadConfigFiles(*self.findConfigFiles(cfg_args))
        self.session.prepareSysPath()
        if cfg_args.load_plugins:
            self.loadPlugins()

    def findConfigFiles(self, cfg_args):
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
        # FIXME pass arguments to session & plugins
        self.testNames = args.testNames

    def loadPlugins(self):
        # FIXME also pass in plugins set via __init__ args
        self.session.loadPlugins(self.defaultPlugins)

    def createTests(self):
        # XXX belongs in init?
        log.debug("Create tests from %s/%s", self.testNames, self.module)
        if self.module and '__unittest' in dir(self.module):
            self.module = None
        self.test = self.testLoader.loadTestsFromNames(
            self.testNames, self.module)

    def runTests(self):
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
