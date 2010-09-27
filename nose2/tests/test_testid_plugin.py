"""Test testid plugin."""
from unittest2 import TestCase
import re
import os.path
import pickle
import shutil
import tempfile

from ..plugins import testid
from ._common import (FakeStartTestEvent, FakeLoadFromNameEvent,
        FakeLoadFromNamesEvent)

class UnitTestTestId(TestCase):
    """Test class TestId.

    Tests are carried out in a temporary directory, since TestId stores state
    to file. The temporary directory is removed after testing.
    """
    tags = ['unit']

    def setUp(self):
        super(UnitTestTestId, self).setUp()
        self._orig_dir = os.getcwd()
        # XXX: Use deterministic temporary directory, which can be inspected
        # after test?
        self._temp_dir = tempfile.mkdtemp()
        os.chdir(self._temp_dir)

    def tearDown(self):
        super(UnitTestTestId, self).tearDown()
        os.chdir(self._orig_dir)
        shutil.rmtree(self._temp_dir, ignore_errors=True)

    def test___init__(self):
        """Test the __init__ method."""
        plug = self._create()
        # Test attributes
        for name, exp_val in [('configSection', 'testid'), ('commandLineSwitch',
            ('I', 'with-id', 'Add test ids to output')), ('idfile',
                os.path.abspath('.noseids')), ('ids', {}), ('tests', {}),
                ('id', 0)]:
            try:
                val = getattr(plug, name)
            except AttributeError:
                self.fail('TestId instance doesn\'t have attribute %s' % (name,))
            self.assertEqual(val, exp_val, 'Attribute %s should have value '
                '\'%s\', but has value %s' % (name, exp_val, val))

    def test_start_test(self):
        """Test startTest method."""
        event = FakeStartTestEvent(self)
        plug = self._create()
        plug.startTest(event)

        self.assertEqual(plug.id, 1)
        test_id = self.id()
        self.assertEqual(plug.ids, {1: test_id})
        self.assertEqual(plug.tests, {test_id: 1})
        self.assertEqual(event._fake_messages, [('#1 ', (2,))])

    def test_start_test_twice(self):
        """Test calling startTest twice."""
        event = FakeStartTestEvent(self)
        plug = self._create()
        plug.startTest(event)
        plug.startTest(event)

        self.assertEqual(plug.id, 1)
        test_id = self.id()
        self.assertEqual(plug.ids, {1: test_id})
        self.assertEqual(plug.tests, {test_id: 1})
        msg = ('#1 ', (2,))
        self.assertEqual(event._fake_messages, [msg, msg])

    def test_stop_test_run(self):
        """Test stopTestRun method."""
        plug = self._create()
        plug.startTest(FakeStartTestEvent(self))
        plug.stopTestRun(None)

        fh = open(plug.idfile, 'r')
        try:
            data = pickle.load(fh)
        finally:
            fh.close()
        self.assertEqual(data, {'ids': plug.ids, 'tests': plug.tests})

    def test_load_tests_from_name(self):
        """Test loadTestsFromName method."""
        plug = self._create()
        # By first starting/stopping a test, an ID is assigned by the plugin
        plug.startTest(FakeStartTestEvent(self))
        plug.stopTestRun(None)
        event = FakeLoadFromNameEvent('1')
        plug.loadTestsFromName(event)

        # The numeric ID should be translated to this test's ID
        self.assertEqual(event.name, self.id())

    def test_load_tests_from_name_no_ids(self):
        """Test calling loadTestsFromName when no IDs have been saved."""
        plug = self._create()
        event = FakeLoadFromNameEvent('1')
        plug.loadTestsFromName(event)

        # The event's name should be unchanged, since no IDs should be mapped
        self.assertEqual(event.name, '1')

    def test_load_tests_from_names(self):
        """Test loadTestsFromNames method."""
        plug = self._create()
        # By first starting/stopping a test, an ID is assigned by the plugin
        plug.startTest(FakeStartTestEvent(self))
        plug.stopTestRun(None)
        event = FakeLoadFromNamesEvent(['1', '2'])
        plug.loadTestsFromNames(event)

        name1, name2 = event.names
        # The first numeric ID should be translated to this test's ID
        self.assertEqual(name1, self.id())
        # The second one should not have a match
        self.assertEqual(name2, '2')

    def _create(self):
        """Create a TestId instance."""
        return testid.TestId()
