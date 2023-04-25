"""
Output test reports in junit-xml format.

This plugin implements :func:`startTest`, :func:`testOutcome` and
:func:`stopTestRun` to compile and then output a test report in
junit-xml format. By default, the report is written to a file called
``nose2-junit.xml`` in the current working directory.

You can configure the output filename by setting ``path`` in a ``[junit-xml]``
section in a config file.  Unicode characters which are invalid in XML 1.0
are replaced with the ``U+FFFD`` replacement character. In the case that your
software throws an error with an invalid byte string.

By default, the ranges of discouraged characters are replaced as well. This can
be changed by setting the ``keep_restricted`` configuration variable to
``True``.

By default, the arguments of parametrized and generated tests are not printed.
For instance, the following code:

.. code-block:: python

    # a.py

    from nose2 import tools

    def test_gen():
        def check(a, b):
            assert a == b, '{}!={}'.format(a,b)

        yield check, 99, 99
        yield check, -1, -1

    @tools.params('foo', 'bar')
    def test_params(arg):
        assert arg in ['foo', 'bar', 'baz']

Produces this XML by default:

.. code-block:: xml

    <testcase classname="a" name="test_gen:1" time="0.000171"
     timestamp="2021-12-09T21:28:09.686611">
        <system-out />
    </testcase>
    <testcase classname="a" name="test_gen:2" time="0.000202"
     timestamp="2021-12-09T21:28:09.686813">
        <system-out />
    </testcase>
    <testcase classname="a" name="test_params:1" time="0.000159"
     timestamp="2021-12-09T21:28:09.686972">
        <system-out />
    </testcase>
    <testcase classname="a" name="test_params:2" time="0.000163"
     timestamp="2021-12-09T21:28:09.687135">
        <system-out />
    </testcase>

But if ``test_fullname`` is ``True``, then the following XML is
produced:

.. code-block:: xml

    <testcase classname="a" name="test_gen:1 (99, 99)" time="0.000213"
     timestamp="2021-12-09T21:28:09.686611">
        <system-out />
    </testcase>
    <testcase classname="a" name="test_gen:2 (-1, -1)" time="0.000194"
     timestamp="2021-12-09T21:28:09.687105">
        <system-out />
    </testcase>
    <testcase classname="a" name="test_params:1 ('foo')" time="0.000178"
     timestamp="2021-12-09T21:28:09.687283">
        <system-out />
    </testcase>
    <testcase classname="a" name="test_params:2 ('bar')" time="0.000187"
     timestamp="2021-12-09T21:28:09.687470">
        <system-out />
    </testcase>

"""
# Based on unittest2/plugins/junitxml.py,
# which is itself based on the junitxml plugin from py.test

import datetime
import json
import os.path
import re
import sys
import time
from xml.etree import ElementTree as ET

from nose2 import events, result, util

__unittest = True


class JUnitXmlReporter(events.Plugin):
    """Output junit-xml test report to file"""

    configSection = "junit-xml"
    commandLineSwitch = ("X", "junit-xml", "Generate junit-xml output report")

    def __init__(self):
        # Read argument from configuration file, or filled with default
        self.path = os.path.realpath(
            self.config.as_str("path", default="nose2-junit.xml")
        )
        self.keep_restricted = self.config.as_bool("keep_restricted", default=False)
        self.test_properties = self.config.as_str("test_properties", default=None)
        self.test_fullname = self.config.as_bool("test_fullname", default=False)

        if self.test_properties is not None:
            self.test_properties_path = os.path.realpath(self.test_properties)
        self.errors = 0
        self.failed = 0
        self.skipped = 0
        self.numtests = 0
        self.tree = ET.Element("testsuite")
        self._start = None

        # Allow user to override certain option from command line
        group = self.session.pluginargs
        group.add_argument(
            "--junit-xml-path",
            action="store",
            default="",
            metavar="FILE",
            dest="path",
            help="Output XML filename",
        )

    def handleArgs(self, event):
        """Read option from command line and override the value in config file
        when necessary"""
        if event.args.path:
            # register if `--junit-xml-path` is given
            # this avoids a situation in which a plugin-related option is given
            # but the plugin isn't activated, which can be confusing (see #521)
            self.register()
            self.path = os.path.realpath(event.args.path)

    def startTest(self, event):
        """Count test, record start time"""
        self.numtests += 1
        self._start = event.startTime

    def testOutcome(self, event):
        """Add test outcome to xml tree"""
        test = event.test
        testid_lines = test.id().split("\n")
        testid = testid_lines[0]
        parts = testid.split(".")
        classname = ".".join(parts[:-1])
        method = parts[-1]
        # for generated test cases
        if len(testid_lines) > 1 and self.test_fullname:
            test_args = ":".join(testid_lines[1:])
            method = f"{method} ({test_args})"

        # subtests do not report success
        if event.outcome == result.SUBTEST and event.exc_info is None:
            return

        testcase = ET.SubElement(self.tree, "testcase")
        testcase.set("timestamp", self._iso_timestamp())
        testcase.set("time", "%.6f" % self._time())
        if not classname:
            classname = test.__module__
        testcase.set("classname", classname)
        testcase.set("name", method)

        msg = ""
        if event.exc_info:
            msg = util.exc_info_to_string(event.exc_info, test)
        elif event.reason:
            msg = event.reason

        msg = string_cleanup(msg, self.keep_restricted)

        if event.outcome == result.ERROR:
            self.errors += 1
            error = ET.SubElement(testcase, "error")
            error.set("message", "test failure")
            error.text = msg
        elif event.outcome == result.FAIL and not event.expected:
            self.failed += 1
            failure = ET.SubElement(testcase, "failure")
            failure.set("message", "test failure")
            failure.text = msg
        elif event.outcome == result.PASS and not event.expected:
            self.skipped += 1
            skipped = ET.SubElement(testcase, "skipped")
            skipped.set("message", "test passes unexpectedly")
        elif event.outcome == result.SKIP:
            self.skipped += 1
            skipped = ET.SubElement(testcase, "skipped")
            if msg:
                skipmsg = "test skipped"
                if event.reason:
                    skipmsg = f"test skipped: {event.reason}"
                skipped.set("message", skipmsg)
                skipped.text = msg
        elif event.outcome == result.FAIL and event.expected:
            self.skipped += 1
            skipped = ET.SubElement(testcase, "skipped")
            skipped.set("message", "expected test failure")
            skipped.text = msg
        elif event.outcome == result.SUBTEST:
            if issubclass(event.exc_info[0], event.test.failureException):
                self.failed += 1
                failure = ET.SubElement(testcase, "failure")
                failure.set("message", "test failure")
                failure.text = msg
            else:
                self.errors += 1
                error = ET.SubElement(testcase, "error")
                error.set("message", "test failure")
                error.text = msg

        system_out = ET.SubElement(testcase, "system-out")
        system_out.text = string_cleanup(
            "\n".join(event.metadata.get("logs", "")), self.keep_restricted
        )

    def _check(self):
        if not os.path.exists(os.path.dirname(self.path)):
            raise OSError(
                2, "JUnitXML: Parent folder does not exist for file", self.path
            )
        if self.test_properties is not None:
            if not os.path.exists(self.test_properties_path):
                raise OSError(
                    2,
                    "JUnitXML: Properties file does not exist",
                    self.test_properties_path,
                )

    def stopTestRun(self, event):
        """Output xml tree to file"""
        self.tree.set("name", "nose2-junit")
        self.tree.set("errors", str(self.errors))
        self.tree.set("failures", str(self.failed))
        self.tree.set("skipped", str(self.skipped))
        self.tree.set("tests", str(self.numtests))
        self.tree.set("time", "%.3f" % event.timeTaken)

        self._check()
        self._include_test_properties()
        self._indent_tree(self.tree)

        output = ET.ElementTree(self.tree)
        output.write(self.path, encoding="utf-8")

    def _include_test_properties(self):
        """Include test properties in xml tree"""
        if self.test_properties is None:
            return

        props = {}
        with open(self.test_properties_path) as data:
            try:
                props = json.loads(data.read())
            except ValueError:
                raise ValueError(
                    "JUnitXML: could not decode file: '%s'" % self.test_properties_path
                )

        properties = ET.SubElement(self.tree, "properties")
        for key, val in props.items():
            prop = ET.SubElement(properties, "property")
            prop.set("name", key)
            prop.set("value", val)

    def _indent_tree(self, elem, level=0):
        """In-place pretty formatting of the ElementTree structure."""
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for e in elem:
                self._indent_tree(e, level + 1)
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
        return 0

    def _iso_timestamp(self):
        # in some cases, `self._start` is still None when this runs, convert to 0
        # see: https://github.com/nose-devs/nose2/pull/505
        timestamp = self._start or 0
        return str(datetime.datetime.utcfromtimestamp(timestamp).isoformat())


#
# xml utility functions
#

# etree outputs XML 1.0 so the 1.1 Restricted characters are invalid.
# and there are no characters that can be given as entities aside
# form & < > ' " which ever have to be escaped (etree handles these fine)
ILLEGAL_RANGES = [
    (0x00, 0x08),
    (0x0B, 0x0C),
    (0x0E, 0x1F),
    (0xD800, 0xDFFF),
    (0xFFFE, 0xFFFF),
]
# 0xD800 thru 0xDFFF are technically invalid in UTF-8 but PY2 will encode
# bytes into these but PY3 will do a replacement

# Other non-characters which are not strictly forbidden but
# discouraged.
RESTRICTED_RANGES = [(0x7F, 0x84), (0x86, 0x9F), (0xFDD0, 0xFDDF)]
# check for a wide build
if sys.maxunicode > 0xFFFF:
    RESTRICTED_RANGES += [
        (0x1FFFE, 0x1FFFF),
        (0x2FFFE, 0x2FFFF),
        (0x3FFFE, 0x3FFFF),
        (0x4FFFE, 0x4FFFF),
        (0x5FFFE, 0x5FFFF),
        (0x6FFFE, 0x6FFFF),
        (0x7FFFE, 0x7FFFF),
        (0x8FFFE, 0x8FFFF),
        (0x9FFFE, 0x9FFFF),
        (0xAFFFE, 0xAFFFF),
        (0xBFFFE, 0xBFFFF),
        (0xCFFFE, 0xCFFFF),
        (0xDFFFE, 0xDFFFF),
        (0xEFFFE, 0xEFFFF),
        (0xFFFFE, 0xFFFFF),
        (0x10FFFE, 0x10FFFF),
    ]

ILLEGAL_REGEX_STR = (
    "[" + "".join([f"{chr(lo)}-{chr(hi)}" for (lo, hi) in ILLEGAL_RANGES]) + "]"
)
RESTRICTED_REGEX_STR = (
    "[" + "".join([f"{chr(lo)}-{chr(hi)}" for (lo, hi) in RESTRICTED_RANGES]) + "]"
)

_ILLEGAL_REGEX = re.compile(ILLEGAL_REGEX_STR, re.U)
_RESTRICTED_REGEX = re.compile(RESTRICTED_REGEX_STR, re.U)


def string_cleanup(string, keep_restricted=False):
    if not issubclass(type(string), str):
        string = str(string, encoding="utf-8", errors="replace")

    string = _ILLEGAL_REGEX.sub("\uFFFD", string)
    if not keep_restricted:
        string = _RESTRICTED_REGEX.sub("\uFFFD", string)

    return string
