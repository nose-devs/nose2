import logging
import os
import sys

from nose2.compat import unittest
from nose2 import events, loader, runner, session


log = logging.getLogger(__name__)


class PluggableTestProgram(unittest.TestProgram):
    sessionClass = session.Session
    loaderClass = loader.PluggableTestLoader
    runnerClass = runner.PluggableTestRunner

    # XXX override __init__ to warn that testLoader and testRunner are ignored?

    def parseArgs(self, argv):
        log.debug("parse argv %s", argv)
        self.session = self.sessionClass()
        self.argparse = self.session.argparse # for convenience

        # XXX force these? or can it be avoided?
        self.testLoader = self.loaderClass(self.session)

        # Parse initial arguments like config file paths, verbosity
        self.setInitialArguments()
        cfg_args, argv = self.argparse.parse_known_args(argv)
        self.handleCfgArgs(cfg_args)

        # Parse arguments for plugins (if any) and test names
        self.argparse.add_argument('testNames', nargs='*')
        args, argv = self.argparse.parse_known_args(argv)
        if argv:
            self.argparse.error("Unrecognized arguments: %s" % ' '.join(argv))
        self.handleArgs(args)
        self.createTests()

    def setInitialArguments(self):
        self.argparse.add_argument('--config', '-c', nargs='?', action='append',
                                 default=['unittest.cfg', 'nose2.cfg'])
        self.argparse.add_argument('--no-user-config', action='store_const',
                                 dest='user_config', const=False, default=True)
        self.argparse.add_argument('--no-plugins', action='store_const',
                                 dest='load_plugins', const=False, default=True)
        self.argparse.add_argument('--verbose', '-v', action='count')
        self.argparse.add_argument('--quiet', action='store_const',
                                 dest='verbose', const=0)

    def handleCfgArgs(self, cfg_args):
        self.session.loadConfigFiles(*self.findConfigFiles(cfg_args))
        if cfg_args.load_plugins:
            self.loadPlugins()
        # FIXME set verbosity

    def findConfigFiles(self, cfg_args):
        filenames = cfg_args.config[:]
        if cfg_args.user_config:
            opts = ('unittest.cfg', 'nose2.cfg', '.unittest.cfg', '.nose2.cfg')
            for fn in opts:
                filenames.append(os.path.expanduser(fn))
        return filenames

    def handleArgs(self, args):
        # FIXME activate or deactivate plugins,
        # pass arguments to plugins that want them
        self.testNames = args.testNames

    def loadPlugins(self):
        # FIXME pass in plugins set via __init__ args
        # FIXME pass in default plugins
        self.session.loadPlugins()

    def createTests(self):
        # fire plugin hook
        event = events.CreateTestsEvent(
            self.testLoader, self.testNames, self.module)
        result = self.session.hooks.createTests(event)
        if event.handled:
            self.test = result
        else:
            if self.testNames is None:
                self.test = self.testLoader.loadTestsFromModule(self.module)
            else:
                self.test = self.testLoader.loadTestsFromNames(self.testNames)

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
