from nose2 import session
from nose2.tests._common import TestCase, Conn
from nose2.plugins import mp


class TestMPPlugin(TestCase):
    def setUp(self):
        self.session = session.Session()
        self.plugin = mp.MultiProcess(session=self.session)

    def test_gentests(self):
        conn = Conn([1, 2, 3])
        res = []
        for x in mp.gentests(conn):
            res.append(x)
        self.assertEqual(res, [1, 2, 3])

    def test_recording_plugin_interface(self):
        rpi = mp.RecordingPluginInterface()
        # this one should record
        rpi.setTestOutcome(None)
        # none of these should record
        rpi.getTestCaseNames(None)
        rpi.startSubprocess(None)
        rpi.stopSubprocess(None)
        rpi.registerInSubprocess(None)
        rpi.loadTestsFromModule(None)
        rpi.loadTestsFromTestCase(None)
        self.assertEqual(rpi.flush(), [('setTestOutcome', None)])
