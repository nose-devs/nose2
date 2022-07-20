import re
from textwrap import dedent
from unittest import mock

from nose2 import collector
from nose2.tests._common import RedirectStdStreams, TestCase


class TestCollector(TestCase):
    _RUN_IN_TEMP = True
    tags = ["unit"]

    def test_collector_completes_with_no_tests(self):
        with open("unittest.cfg", "w") as ut_file:
            ut_file.write(
                dedent(
                    """
                [unittest]
                quiet = true
            """
                )
            )
        test = collector.collector()
        with RedirectStdStreams() as redir:
            self.assertRaises(SystemExit, test.run, None)
        self.assertEqual("", redir.stdout.getvalue())
        self.assertTrue(
            re.match(
                r"\n-+\nRan 0 tests in \d.\d\d\ds\n\nOK\n", redir.stderr.getvalue()
            )
        )

    def test_collector_sets_testLoader_in_session(self):
        """
        session.testLoader needs to be set so that plugins that use this
        field (like Layers) dont break.
        """
        test = collector.collector()
        mock_session = mock.MagicMock()
        mock_loader = mock.MagicMock()
        mock_runner = mock.MagicMock()
        test._get_objects = mock.Mock(
            return_value=(mock_session, mock_loader, mock_runner)
        )
        test._collector(None)
        self.assertTrue(mock_session.testLoader is mock_loader)
