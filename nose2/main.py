import os

from unittest2.main import TestProgram, USAGE_AS_MAIN

from . import plugins


def main_():
    TestProgram.USAGE = USAGE_AS_MAIN
    TestProgram(module=None, buffer=True, config=plugins.configFile())
