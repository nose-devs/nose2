from nose2 import events


class PrintFixture(events.Plugin):
    alwaysOn = True

    def startLayerSetup(self, event):
        print(f"StartLayerSetup: {event.layer}")

    def stopLayerSetup(self, event):
        print(f"StopLayerSetup: {event.layer}")

    def startLayerSetupTest(self, event):
        log = "StartLayerSetupTest: {0}:{1}"
        print(log.format(event.layer, event.test))

    def stopLayerSetupTest(self, event):
        log = "StopLayerSetupTest: {0}:{1}"
        print(log.format(event.layer, event.test))

    def startLayerTeardownTest(self, event):
        log = "StartLayerTeardownTest: {0}:{1}"
        print(log.format(event.layer, event.test))

    def stopLayerTeardownTest(self, event):
        log = "StopLayerTeardownTest: {0}:{1}"
        print(log.format(event.layer, event.test))

    def startLayerTeardown(self, event):
        print(f"StartLayerTeardown: {event.layer}")

    def stopLayerTeardown(self, event):
        print(f"StopLayerTeardown: {event.layer}")
