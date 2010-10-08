from unittest2.events import hooks, Plugin

class Outcomes(Plugin):
    """TODO: document"""

    configSection = 'outcomes'

    def __init__(self):
        self.treat_as_fail = set(self.config.as_list('treat-as-fail', []))
        self.treat_as_skip = set(self.config.as_list('treat-as-skip', []))
        self.register()

    def stopTest(self, event):
        if event.exc_info:
            ec, ev, tb = event.exc_info
            classname = ec.__name__
            if classname in self.treat_as_fail:
                short, long_ = self.labels(classname)
                event.setOutcome(long_, 'failed', short, long_)
            elif classname in self.treat_as_skip:
                short, long_ = self.labels(classname, upper=False)
                event.setOutcome(
                    long_, 'skipped', short, "%s '%%s'" % long_, ev)

    def labels(self, label, upper=True):
        if upper:
            label = label.upper()
        else:
            label = label.lower()
        short = label[0]
        return short, label
