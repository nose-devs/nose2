import os

from nose2.compat import unittest
from nose2 import session


class PluggableTestProgram(unittest.TestProgram):

    def parseArgs(self, argv):
        self.session = session.Session()
        self.argparse = self.session.argparse # for convenience

        # Parse initial arguments like config file paths, verbosity
        self.setInitialArguments()
        cfg_args, argv = self.argparse.parse_args(argv)
        self.handleCfgArgs(cfg_args)

        # Parse arguments for plugins (if any) and test names
        self.argparse.add_argument('tests', nargs='*')
        args, argv = self.argparse.parse_args(argv)
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
        pass

    def loadPlugins(self):
        # FIXME pass in plugins set via __init__ args
        self.session.loadPlugins()

    def createTests(self):
        # fire plugin hook
        pass

    def runTests(self):
        # fire plugin hook
        pass

main_ = PluggableTestProgram
