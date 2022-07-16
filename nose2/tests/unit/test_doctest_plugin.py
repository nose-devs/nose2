"""Test doctests plugin."""
import doctest
from textwrap import dedent

from nose2 import events, loader, session
from nose2.plugins import doctests
from nose2.tests._common import TestCase


class UnitTestDocTestLoader(TestCase):

    """Test class DocTestLoader."""

    tags = ["unit"]

    _RUN_IN_TEMP = True

    def setUp(self):
        self.session = session.Session()
        self.loader = loader.PluggableTestLoader(self.session)
        self.plugin = doctests.DocTestLoader(session=self.session)
        super().setUp()

    def test___init__(self):
        """Test the __init__ method."""
        self.assertEqual(self.plugin.extensions, [".txt", ".rst"])

    def test_handle_file(self):
        """Test method handleFile."""
        # Create doctest files of supported types
        doc_test = """\
>>> 2 == 2
True
"""
        txt_event = self._handle_file("docs.txt", doc_test)
        rst_event = self._handle_file("docs.rst", doc_test)
        # Exercise loading of doctests from Python code
        py_event = self._handle_file(
            "docs.py",
            """\
\"\"\"
>>> 2 == 2
True
\"\"\"
""",
        )
        for event, ext in [(txt_event, "txt"), (rst_event, "rst")]:
            (test,) = event.extraTests
            self.assertTrue(isinstance(test, doctest.DocFileCase))
            self.assertEqual(repr(test), "docs.%s" % ext)

        (testsuite,) = py_event.extraTests
        (test,) = list(testsuite)
        self.assertEqual(repr(test), "docs ()")

    def test_handle_file_python_without_doctests(self):
        """Test calling handleFile for a Python module without doctests."""
        event = self._handle_file(
            "mod.py",
            """\
def func():
    pass
""",
        )
        self.assertEqual(event.extraTests, [doctest.DocTestSuite()])

    def test_handle_file_python_setup_py(self):
        # Test calling handleFile on a top-level setup.py file.
        # The file should be ignored by the plugin as it cannot safely be
        # imported.

        setup_py = dedent(
            """\
            '''
            >>> never executed
            '''
            from setuptools import setup
            setup(name='foo')
            """
        )
        event = self._handle_file("setup.py", setup_py)
        self.assertEqual(event.extraTests, [])

    def _handle_file(self, fpath, content):
        """Have plugin handle a file with certain content.

        The file is created, then a plugin is instantiated and its handleFile
        method is called for the file.
        """
        fh = open(fpath, "w")
        try:
            fh.write(content)
        finally:
            fh.close()

        event = events.HandleFileEvent(self.loader, fh.name, fpath, None, None)
        self.plugin.handleFile(event)
        return event
