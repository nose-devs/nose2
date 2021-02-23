"""
test of some commands
"""
import logging

from nose2.events import Plugin

log = logging.getLogger(__name__)


class PluginEssai(Plugin):
    configSection = 'essai'
    commandLineSwitch = ('e', 'with-essai', 'Essai de plugin')

    def __init__(self):
        pass
