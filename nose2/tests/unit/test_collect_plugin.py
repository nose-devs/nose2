from nose2.tests._common import FakeStartTestRunEvent, TestCase
from nose2.plugins import collect


class TestCollectOnly(TestCase):
    tags = ['unit']

    def setUp(self):
        self.plugin = collect.CollectOnly()

    def test_startTestRun_sets_executeTests(self):
        event = FakeStartTestRunEvent()
        self.plugin.startTestRun(event)
        self.assertEqual(event.executeTests, self.plugin.collectTests)


