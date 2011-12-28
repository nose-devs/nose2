import unittest2

from ..plugins import outcomes

class TestOutComesPlugin(unittest2.TestCase):
    tags = ['unit']

    def setUp(self):
        self.plugin = outcomes.Outcomes()

    def test_labels_upper(self):
        self.assertEqual(self.plugin.labels('xxx'), ('X', 'XXX'))
