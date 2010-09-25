"""Test doctests plugin."""
import doctest

from ..plugins import doctests

from ._common import TestCase, FakeHandleFileEvent


class UnitTestDocTestLoader(TestCase):
    """Test class DocTestLoader."""
    tags = ['unit']

    _RUN_IN_TEMP = True

    def test___init__(self):
        """Test the __init__ method."""
        plug = self.__create()

        self.assertEqual(plug.extensions, ['.txt', '.rst'])


    def test_handle_file(self):
        """Test method handleFile."""
        # Create doctest files of supported types
        plug = self.__create()
        doc_test = """\
>>> 2 == 2
True
"""
        for ext in ['txt', 'rst']:
            fh = open('docs.%s' % ext, 'wb')
            try:
                fh.write(doc_test)
            finally:
                fh.close()

            event = FakeHandleFileEvent(fh.name)
            plug.handleFile(event)

            test, = event.extraTests
            self.assertTrue(isinstance(test, doctest.DocFileCase))
            self.assertEqual(repr(test), fh.name)


    def __create(self):
        """Create a DocTestLoader instance."""
        plug = doctests.DocTestLoader()
        return plug
