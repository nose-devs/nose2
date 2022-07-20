"""
Load tests from doctests.

This plugin implements :func:`handleFile` to load doctests from text files
and python modules.

To disable loading doctests from text files, configure an empty extensions list:

.. code-block :: ini

  [doctest]
  extensions =

"""
import doctest
import os

from nose2 import util
from nose2.events import Plugin

__unittest = True


class DocTestLoader(Plugin):
    configSection = "doctest"
    commandLineSwitch = (
        None,
        "with-doctest",
        "Load doctests from text files and modules",
    )

    def __init__(self):
        self.extensions = self.config.as_list("extensions", [".txt", ".rst"])

    def handleFile(self, event):
        """Load doctests from text files and modules"""
        path = event.path
        _root, ext = os.path.splitext(path)
        if ext in self.extensions:
            suite = doctest.DocFileTest(path, module_relative=False)
            event.extraTests.append(suite)
            return
        elif not util.valid_module_name(os.path.basename(path)):
            return

        name, package_path = util.name_from_path(path)
        # ignore top-level setup.py which cannot be imported
        if name == "setup":
            return
        util.ensure_importable(package_path)
        try:
            module = util.module_from_name(name)
        except Exception:
            # XXX log warning here?
            return
        if hasattr(module, "__test__") and not module.__test__:
            return
        suite = doctest.DocTestSuite(module)
        event.extraTests.append(suite)
