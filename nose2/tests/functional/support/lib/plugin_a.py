from nose2 import events


class PluginA(events.Plugin):
    configSection = "a"

    def __init__(self) -> None:
        self.a = self.config.as_int("a", 0)
