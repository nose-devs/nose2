from nose2.plugins import outcomes
from nose2.tests._common import TestCase


class TestOutComesPlugin(TestCase):
    tags = ['unit']

    def setUp(self):
        self.plugin = outcomes.Outcomes()

    def test_labels_upper(self):
        self.assertEqual(self.plugin.labels('xxx'), ('X', 'XXX'))
