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
import time, re, sys, six
from xml.etree import ElementTree as ET

from nose2 import events, result, util
from six import u

def _unichr(string):
    if six.PY3:
        return chr(string)
    else:
        return unichr(string)

__unittest = True

_illegal_xml_rngs = [ (0x00, 0x08), (0x0B, 0x0C), (0x0E, 0x1F), (0x7F, 0x84), 
                    (0x86, 0x9F), (0xD800, 0xDFFF), (0xFDD0, 0xFDDF), 
                    (0xFFFE, 0xFFFF), (0x1FFFE, 0x1FFFF), (0x2FFFE, 0x2FFFF), 
                    (0x3FFFE, 0x3FFFF), (0x4FFFE, 0x4FFFF), (0x5FFFE, 0x5FFFF),
                    (0x6FFFE, 0x6FFFF), (0x7FFFE, 0x7FFFF), (0x8FFFE, 0x8FFFF),
                    (0x9FFFE, 0x9FFFF), (0xAFFFE, 0xAFFFF), (0xBFFFE, 0xBFFFF),
                    (0xCFFFE, 0xCFFFF), (0xDFFFE, 0xDFFFF), (0xEFFFE, 0xEFFFF),
                    (0xFFFFE, 0xFFFFF), (0x10FFFE, 0x10FFFF) ]

_illegal_xml_rngs = [ (l, min(h, sys.maxunicode)) for (l,h) \
    	                                  in _illegal_xml_rngs \
                                                  if l < sys.maxunicode ]
_illegal_xml_restr = u('[') + \
                     u('').join(["%s-%s" % (_unichr(l), _unichr(h)) 
                               for (l, h) in _illegal_xml_rngs]) + \
                     u(']')

_illegal_xml_re = re.compile(_illegal_xml_restr)

def _match_repr(match):
    """gets the string reprentation and strips off u'' if needed""" 
    value = repr(match.group())
    if value[0:2] == "u'" and value[-1:] == "'":
        value = value[2:-1]
    elif value[0] == "'" and value[-1:] == "'":
        value = value[1:-1]

    return value

def xml_string_cleanup(string):
    if not six.PY3:
        string = unicode(string, errors='replace')
    return _illegal_xml_re.sub(_match_repr, string)

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

        msg = xml_string_cleanup(msg)

	

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
