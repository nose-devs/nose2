# This module contains some code copied from unittest2/loader.py and other
# code developed in reference to that module and others within unittest2.

# unittest2 is Copyright (c) 2001-2010 Python Software Foundation; All
# Rights Reserved. See: http://docs.python.org/license.html

import logging
import os
import types
import re
import sys
import traceback
import platform
import six
import inspect
from inspect import isgeneratorfunction


__unittest = True
IDENT_RE = re.compile(r'^[_a-zA-Z]\w*$', re.UNICODE)
VALID_MODULE_RE = re.compile(r'[_a-zA-Z]\w*\.py$', re.UNICODE)


def ln(label, char='-', width=70):
    """Draw a divider, with ``label`` in the middle.

    >>> ln('hello there')
    '---------------------------- hello there -----------------------------'

    ``width`` and divider ``char`` may be specified. Defaults are ``70`` and ``'-'``,
    respectively.

    """
    label_len = len(label) + 2
    chunk = (width - label_len) // 2
    out = '%s %s %s' % (char * chunk, label, char * chunk)
    pad = width - len(out)
    if pad > 0:
        out = out + (char * pad)
    return out


def valid_module_name(path):
    """Is ``path`` a valid module name?"""
    return VALID_MODULE_RE.search(path)


def name_from_path(path):
    """Translate ``path`` into module name

    Returns a two-element tuple:

    1. a dotted module name that can be used in an import statement
       (e.g., ``pkg1.test.test_things``)

    2. a full path to filesystem directory, which must be on ``sys.path``
       for the import to succeed.

    """
    # back up to find module root
    parts = []
    path = os.path.normpath(path)
    base = os.path.splitext(path)[0]
    candidate, top = os.path.split(base)
    parts.append(top)
    while candidate:
        if ispackage(candidate):
            candidate, top = os.path.split(candidate)
            parts.append(top)
        else:
            break
    return '.'.join(reversed(parts)), candidate


def module_from_name(name):
    """Import module from ``name``"""
    __import__(name)
    return sys.modules[name]


def test_from_name(name, module):
    """Import test from ``name``"""
    pos = name.find(':')
    index = None
    if pos != -1:
        real_name, digits = name[:pos], name[pos + 1:]
        try:
            index = int(digits)
        except ValueError:
            pass
        else:
            name = real_name
    parent, obj = object_from_name(name, module)
    return parent, obj, name, index


def object_from_name(name, module=None):
    """
    Given a dotted name, return the corresponding object.

    Getting the object can fail for two reason:

        - the object is a module that cannot be imported.
        - the object is a class or a function that does not exists.

    Since we cannot distinguish between these two cases, we assume we are in
    the first one. We expect the stacktrace is explicit enough for the user to
    understand the error.
    """
    import_error = None
    parts = name.split('.')
    if module is None:
        (module, import_error) = try_import_module_from_name(parts[:])
        parts = parts[1:]
    parent = None
    obj = module
    for part in parts:
        try:
            parent, obj = obj, getattr(obj, part)
        except AttributeError as e:
            if is_package_or_module(obj) and import_error:
                # Re-raise the import error which got us here, since
                # it probably better describes the issue.
                _raise_custom_attribute_error(obj, part, e, import_error)
            else:
                raise

    return parent, obj


def _raise_custom_attribute_error(obj, attr, attr_error_exc, prev_exc):

    if sys.version_info >= (3, 0):
        six.raise_from(attr_error_exc, prev_exc[1])

    # for python 2, do exception chaining manually
    raise AttributeError(
        "'%s' has not attribute '%s'\n\nMaybe caused by\n\n%s" % (
            obj, attr, '\n'.join(traceback.format_exception(*prev_exc))))


def is_package_or_module(obj):
    if hasattr(obj, '__path__') or isinstance(obj, types.ModuleType):
        return True
    return False


def try_import_module_from_name(splitted_name):
    """
    Try to find the longest importable from the ``splitted_name``, and return
    the corresponding module, as well as the potential ``ImportError``
    exception that occurs when trying to import a longer name.

    For instance, if ``splitted_name`` is ['a', 'b', 'c'] but only ``a.b`` is
    importable, this function:
    
        1. tries to import ``a.b.c`` and fails
        2. tries to import ``a.b`` and succeeds
        3. return ``a.b`` and the exception that occured at step 1.
    """
    module = None
    import_error = None
    while splitted_name:
        try:
            module = __import__('.'.join(splitted_name))
            break
        except:
            import_error = sys.exc_info()
            del splitted_name[-1]
            if not splitted_name:
                six.reraise(*sys.exc_info())
    return (module, import_error)


def name_from_args(name, index, args):
    """Create test name from test args"""
    summary = ', '.join(repr(arg) for arg in args)
    return '%s:%s\n%s' % (name, index + 1, summary[:79])


def test_name(test, qualname=True):
    # XXX does not work for test funcs; test.id() lacks module
    if hasattr(test, '_funcName'):
        tid = test._funcName
    elif hasattr(test, '_testFunc'):
        tid = "%s.%s" % (test._testFunc.__module__, test._testFunc.__name__)
    else:
        if sys.version_info >= (3, 5) and not qualname:
            test_module = test.__class__.__module__
            test_class = test.__class__.__name__
            test_method = test._testMethodName
            tid = "%s.%s.%s" % (test_module, test_class, test_method)
        else:
            tid = test.id()
    if '\n' in tid:
        tid = tid.split('\n')[0]
    return tid


def ispackage(path):
    """Is this path a package directory?"""
    if os.path.isdir(path):
        # at least the end of the path must be a legal python identifier
        # and __init__.py[co] must exist
        end = os.path.basename(path)
        if IDENT_RE.match(end):
            for init in ('__init__.py', '__init__.pyc', '__init__.pyo'):
                if os.path.isfile(os.path.join(path, init)):
                    return True
            if sys.platform.startswith('java') and \
                    os.path.isfile(os.path.join(path, '__init__$py.class')):
                return True
    return False


def ensure_importable(dirname):
    """Ensure a directory is on ``sys.path``."""
    if dirname not in sys.path:
        sys.path.insert(0, dirname)


def isgenerator(obj):
    """Is this object a generator?"""
    return (isgeneratorfunction(obj)
            or getattr(obj, 'testGenerator', None) is not None)


def has_module_fixtures(test):
    """Does this test live in a module with module fixtures?"""
    modname = test.__class__.__module__
    try:
        mod = sys.modules[modname]
    except KeyError:
        return
    return hasattr(mod, 'setUpModule') or hasattr(mod, 'tearDownModule')


def has_class_fixtures(test):
    # hasattr would be the obvious thing to use here. Unfortunately, all tests
    # inherit from unittest2.case.TestCase, and that *always* has setUpClass and
    # tearDownClass methods. Thus, exclude the unitest and unittest2 base
    # classes from the lookup.
    def is_not_base_class(c):
        return (
            "unittest.case" not in c.__module__ and
            "unittest2.case" not in c.__module__)
    has_class_setups = any(
        'setUpClass' in c.__dict__ for c in test.__class__.__mro__ if is_not_base_class(c))
    has_class_teardowns = any(
        'tearDownClass' in c.__dict__ for c in test.__class__.__mro__ if is_not_base_class(c))
    return has_class_setups or has_class_teardowns


def safe_decode(string):
    """Safely decode a byte string into unicode"""
    if string is None:
        return string
    try:
        return string.decode()
    except AttributeError:
        return string
    except UnicodeDecodeError:
        pass
    try:
        return string.decode('utf-8')
    except UnicodeDecodeError:
        return six.u('<unable to decode>')


def safe_encode(string, encoding='utf-8'):
    if string is None:
        return string
    if encoding is None:
        encoding = 'utf-8'
    try:
        return string.encode(encoding)
    except AttributeError:
        return string
    except UnicodeDecodeError:
        # already encoded
        return string
    except UnicodeEncodeError:
        return six.u('<unable to encode>')


def exc_info_to_string(err, test):
    """Format exception info for output"""
    formatTraceback = getattr(test, 'formatTraceback', None)
    if formatTraceback is not None:
        return test.formatTraceback(err)
    else:
        return format_traceback(test, err)


def format_traceback(test, err):
    """Converts a :func:`sys.exc_info` -style tuple of values into a string."""
    exctype, value, tb = err
    if not hasattr(tb, 'tb_next'):
        msgLines = tb
    else:
        # Skip test runner traceback levels
        while tb and _is_relevant_tb_level(tb):
            tb = tb.tb_next
        failure = getattr(test, 'failureException', AssertionError)
        if exctype is failure:
            # Skip assert*() traceback levels
            length = _count_relevant_tb_levels(tb)
            msgLines = traceback.format_exception(exctype, value, tb, length)
        else:
            msgLines = traceback.format_exception(exctype, value, tb)

    return ''.join(msgLines)


def transplant_class(cls, module):
    """Make ``cls`` appear to reside in ``module``.

    :param cls: A class
    :param module: A module name
    :returns: A subclass of ``cls`` that appears to have been defined in ``module``.

    The returned class's ``__name__`` will be equal to
    ``cls.__name__``, and its ``__module__`` equal to ``module``.

    """
    class C(cls):
        pass
    C.__module__ = module
    C.__name__ = cls.__name__
    return C


def parse_log_level(lvl):
    """Return numeric log level given a string"""
    try:
        return int(lvl)
    except ValueError:
        pass
    return getattr(logging, lvl.upper(), logging.WARN)


def _is_relevant_tb_level(tb):
    return '__unittest' in tb.tb_frame.f_globals


def _count_relevant_tb_levels(tb):
    length = 0
    while tb and not _is_relevant_tb_level(tb):
        length += 1
        tb = tb.tb_next
    return length


class _WritelnDecorator(object):

    """Used to decorate file-like objects with a handy :func:`writeln` method"""

    def __init__(self, stream):
        self.stream = stream

    def __getattr__(self, attr):
        if attr in ('stream', '__getstate__'):
            raise AttributeError(attr)
        return getattr(self.stream, attr)

    def write(self, arg):
        if sys.version_info[0] == 2:
            arg = safe_encode(arg, getattr(self.stream, 'encoding', 'utf-8'))
        self.stream.write(arg)

    def writeln(self, arg=None):
        if arg:
            self.write(arg)
        self.write('\n')  # text-mode streams translate to \r\n if needed


def ancestry(layer):
    layers = [[layer]]
    bases = [base for base in bases_and_mixins(layer)
             if base is not object]
    while bases:
        layers.append(bases)
        newbases = []
        for b in bases:
            for bb in bases_and_mixins(b):
                if bb is not object:
                    newbases.append(bb)
        bases = newbases
    layers.reverse()
    return layers


def bases_and_mixins(layer):
    return (layer.__bases__ + getattr(layer, 'mixins', ()))


def num_expected_args(func):
    """Return the number of arguments that :func: expects"""
    if six.PY2:
        return len(inspect.getargspec(func)[0])
    else:
        return len(inspect.getfullargspec(func)[0])


def call_with_args_if_expected(func, *args):
    """Take :func: and call it with supplied :args:, in case that signature expects any.
    Otherwise call the function without any arguments.
    """
    if num_expected_args(func) > 0:
        func(*args)
    else:
        func()
