from nose2.tests._common import FunctionalTestCase


class DecoratorsTests(FunctionalTestCase):
    def test_with_setup(self):
        process = self.runIn(
            'scenario/decorators', 'test_decorators.test_with_setup')

        self.assertTestRunOutputMatches(process, stderr="Ran 1 test")
        self.assertEqual(process.poll(), 0, process.stderr.getvalue())
