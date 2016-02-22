import six
from nose2 import events


class PrintFixture(events.Plugin):
    alwaysOn = True

    def startLayerSetup(self, event):
        six.print_("StartLayerSetup: {0}".format(event.layer))

    def stopLayerSetup(self, event):
        six.print_("StopLayerSetup: {0}".format(event.layer))

    def startLayerSetupTest(self, event):
        log = "StartLayerSetupTest: {0}:{1}"
        six.print_(log.format(event.layer, event.test))

    def stopLayerSetupTest(self, event):
        log = "StopLayerSetupTest: {0}:{1}"
        six.print_(log.format(event.layer, event.test))

    def startLayerTeardownTest(self, event):
        log = "StartLayerTeardownTest: {0}:{1}"
        six.print_(log.format(event.layer, event.test))

    def stopLayerTeardownTest(self, event):
        log = "StopLayerTeardownTest: {0}:{1}"
        six.print_(log.format(event.layer, event.test))

    def startLayerTeardown(self, event):
        six.print_("StartLayerTeardown: {0}".format(event.layer))

    def stopLayerTeardown(self, event):
        six.print_("StopLayerTeardown: {0}".format(event.layer))
