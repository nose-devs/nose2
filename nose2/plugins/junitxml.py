"""
Output test reports in junit-xml format.

This plugin implements :func:`startTest`, :func:`testOutcome` and
:func:`stopTestRun` to compile and then output a test report in
junit-xml format. By default, the report is written to a file called
``nose2-junit.xml`` in the current working directory. You can
configure the output filename by setting ``path`` in a ``[junit-xml]``
section in a config file.

"""
# Based on unittest2/plugins/junitxml.py,
# which is itself based on the junitxml plugin from py.test
import time
from xml.etree import ElementTree as ET

from nose2 import events, result, util


__unittest = True


class JUnitXmlReporter(events.Plugin):
    """Output junit-xml test report to file"""
    configSection = 'junit-xml'
    commandLineSwitch = ('X', 'junit-xml', 'Generate junit-xml output report')

    def __init__(self):
        self.path = self.config.as_str('path', default='nose2-junit.xml')
        self.errors = 0
        self.failed = 0
        self.skipped = 0
        self.numtests = 0
        self.tree = ET.Element('testsuite')
        self._start = None

    def startTest(self, event):
        """Count test, record start time"""
        self.numtests += 1
        self._start = event.startTime

    def testOutcome(self, event):
        """Add test outcome to xml tree"""
        test = event.test
        testid = test.id().split('\n')[0]
        # split into module, class, method parts... somehow
        parts = testid.split('.')
        classname = '.'.join(parts[:-1])
        method = parts[-1]

        testcase = ET.SubElement(self.tree, 'testcase')
        testcase.set('time', "%.6f" % self._time())
        testcase.set('classname', classname)
        testcase.set('name', method)

        msg = ''
        if event.exc_info:
            msg = util.exc_info_to_string(event.exc_info, test)
        elif event.reason:
            msg = event.reason
        if event.outcome == result.ERROR:
            self.errors += 1
            error = ET.SubElement(testcase, 'error')
            error.set('message', 'test failure')
            error.text = msg
        elif event.outcome == result.FAIL and not event.expected:
            self.failed += 1
            failure = ET.SubElement(testcase, 'failure')
            failure.set('message', 'test failure')
            failure.text = msg
        elif event.outcome == result.PASS and not event.expected:
            self.skipped += 1
            skipped = ET.SubElement(testcase, 'skipped')
            skipped.set('message', 'test passes unexpectedly')
        elif event.outcome == result.SKIP:
            self.skipped += 1
            skipped = ET.SubElement(testcase, 'skipped')
        elif event.outcome == result.FAIL and event.expected:
            self.skipped += 1
            skipped = ET.SubElement(testcase, 'skipped')
            skipped.set('message', 'expected test failure')
            skipped.text = msg

    def stopTestRun(self, event):
        """Output xml tree to file"""
        self.tree.set('name', 'nose2-junit')
        self.tree.set('errors', str(self.errors))
        self.tree.set('failures' , str(self.failed))
        self.tree.set('skips', str(self.skipped))
        self.tree.set('tests', str(self.numtests))
        self.tree.set('time', "%.3f" % event.timeTaken)

        self._indent_tree(self.tree)
        output = ET.ElementTree(self.tree)
        output.write(self.path, encoding="utf-8")

    def _indent_tree(self, elem, level=0):
        """In-place pretty formatting of the ElementTree structure."""
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self._indent_tree(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def _time(self):
        try:
            return time.time() - self._start
        except Exception:
            pass
        finally:
            self._start = None
