import os

from unittest2 import main_, config, events

from . import plugins


def nose2_main():
    events.loadPlugins(configLocations=[plugins.configFile()])
    main_()
