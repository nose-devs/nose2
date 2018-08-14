"""
This plugin implements :func:`startTestRun`, which excludes all test objects
that define a ``__testlabels__`` attribute that evaluates to ``False``.
"""
from unittest import TestSuite
from nose2 import events
import logging

LOG = logging.getLogger(__name__)

__unittest = True


class CheckLabels(events.Plugin):
    """
    Exclude all tests defining a ``__testlabels__`` attribute that evaluates to ``False``.
    """
    alwaysOn = True

    def startTestRun(self, event):
        """
        Recurse :attr:`event.suite` and remove all test suites and test cases
        that define a ``__testlabels__`` attribute that evaluates to ``False``.
        """
        self.labels = self.session.labels
        self.match_labels = []
        self.skip_labels = []
        self.parse_labels()

        # search for labels only if either match_labels or skip_labels are detected
        if self.match_labels or self.skip_labels:
            self.removeTests(event.suite)

    def parse_labels(self):
        labels = filter(None, self.labels.split(" "))

        # take skip labels
        """
        Any label with "not" as prefix word will be considered as skip labels
        """
        for i, ele in enumerate(labels):
            if ele == "not":
                self.skip_labels.append(labels.pop(i + 1))
                labels.pop(i)
                if i > 0:
                    labels.pop(i - 1)
        # convert skip labels to set
        self.skip_labels = set(self.skip_labels)

        """
        this logic works as follows
        1. any label with prefix word as "or" will be taken as individual elements
        2. any label(s) with prefix word as "and" will be grouped

        ex 1: labels = "express and controlpath"
           in this case, tests should have both "express" and "controlpath" as labels
           so, we group then as a set, and ensure it is subset of test's labels

        ex 2: labels = "express or controlpath"
           in this case, test labels with express or controlpath or both will be
           considered to run. These will go as individual elements in match_labels
           attribute and if any of the element in match_labels is found in
           test's labels, test will be choosen for running
        """

        # take labels with "or" as prefix word
        labels = " ".join(labels).split("or")
        match_labels = []

        # take the labels that are with "and" as prefix word
        match_labels.extend([ele.strip() for ele in labels if " and" not in ele])
        match_labels.extend([ele.split(" and") for ele in labels if " and" in ele])

        # remove spaces
        for label in match_labels:
            if isinstance(label, list):
                self.match_labels.append([ele.strip() for ele in label if ele.strip()])
            else:
                label = label.strip()
                if label:
                    self.match_labels.append(label)

    def has_skip_label(self, testname, testlabels):
        if self.skip_labels:
            common_labels = list(testlabels.intersection(self.skip_labels))
            if common_labels:
                LOG.debug("%s has skip label(s): %s", testname, common_labels)
                return True
        return False

    def has_match_label(self, testname, testlabels):
        if self.match_labels:
            found = False
            for label in self.match_labels:
                if isinstance(label, list):
                    # evaluate "and" group. all labels in the group should match
                    label = set(label)
                    if not label.issubset(testlabels):
                        missing_labels = list(label.difference(testlabels))
                        LOG.debug("%s doesn't have label(s): %s",
                                  testname, missing_labels)
                        return False
                else:
                    # evaluate "or" group, atleast one label should match
                    if label in testlabels:
                        found = True
            return found
        # no labels specified, all selected tests are runnable
        return True

    def should_run(self, testname, testlabels):
        return (not self.has_skip_label(testname, testlabels)
                and self.has_match_label(testname, testlabels))

    def removeTests(self, suite):
        for test in list(suite):
            if isinstance(test, TestSuite):
                self.removeTests(test)
            else:
                if hasattr(test, '_testMethodName'):
                    testmethod = test._testMethodName
                    fqtest = "{}.{}.{}".format(test.__module__,
                                               test.__class__.__name__,
                                               testmethod)
                    testlabels = getattr(getattr(test, testmethod),
                                         '__testlabels__',
                                         None)
                    if testlabels is not None and \
                            self.should_run(fqtest, testlabels) is False:
                        suite._tests.remove(test)
