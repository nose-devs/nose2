import os

from nose2.compat import unittest
from nose2 import config, options


class PluggableTestProgram(unittest.TestProgram):

    def parseArgs(self, argv):
        self.parser = options.MultipassOptionParser(prog='nose2')
        self.session = config.Session()

        # Parse initial arguments like config file paths, verbosity
        self.setInitialArguments()
        cfg_args, argv = self.parser.parse_args(argv)
        self.handleCfgArgs(cfg_args)

        # Parse arguments for plugins (if any) and test names
        self.parser.add_argument('tests', nargs='*')
        args, argv = self.parser.parse_args(argv)
        if argv:
            self.parser.error("Unrecognized arguments: %s" % ' '.join(argv))
        self.handleArgs(args)
        self.createTests()

    def setInitialArguments(self):
        self.parser.add_argument('--config', '-c', nargs='?', action='append',
                                 default=['unittest.cfg', 'nose2.cfg'])
        self.parser.add_argument('--no-user-config', action='store_const',
                                 dest='user_config', const=False, default=True)
        self.parser.add_argument('--no-plugins', action='store_const',
                                 dest='load_plugins', const=False, default=True)
        self.parser.add_argument('--verbose', '-v', action='count')
        self.parser.add_argument('--quiet', action='store_const',
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
        # load plugins in default plugin list
        # load plugins listed in config files
        # load plugins set via __init__ args
        # remove excluded plugins
        self.session.loadPlugins()

    def createTests(self):
        # fire plugin hook
        pass

    def runTests(self):
        # fire plugin hook
        pass

main_ = PluggableTestProgram
