"""
This module contains some code copied from unittest2/loader.py and other
code developed in reference to that module and others within unittest2.

unittest2 is Copyright (c) 2001-2010 Python Software Foundation; All
Rights Reserved. See: http://docs.python.org/license.html

"""
import os
import re
import sys
import traceback

try:
    from compiler.consts import CO_GENERATOR
except ImportError:
    # IronPython doesn't have a complier module
    CO_GENERATOR=0x20

try:
    from inspect import isgeneratorfunction # new in 2.6
except ImportError:
    import inspect
    # backported from Python 2.6
    def isgeneratorfunction(func):
        return bool((inspect.isfunction(func) or inspect.ismethod(func)) and
                    func.func_code.co_flags & CO_GENERATOR)

import six


IDENT_RE = re.compile(r'^[_a-zA-Z]\w*$', re.UNICODE)
VALID_MODULE_RE = re.compile(r'[_a-zA-Z]\w*\.py$', re.UNICODE)


def ln(label, char='-', width=70):
    """Draw a divider, with label in the middle.

    >>> ln('hello there')
    '---------------------------- hello there -----------------------------'

    Width and divider char may be specified. Defaults are 70 and '-'
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
    return VALID_MODULE_RE.search(path)


def name_from_path(path):
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
    return '.'.join(reversed(parts))


def module_from_name(name):
    __import__(name)
    return sys.modules[name]


def test_from_name(name, module):
    pos = name.find(':')
    index = None
    if pos != -1:
        real_name, digits = name[:pos], name[pos+1:]
        try:
            index = int(digits)
        except ValueError:
            pass
        else:
            name = real_name
    try:
        parent, obj = object_from_name(name, module)
    except (AttributeError, ImportError):
        return None
    return parent, obj, name, index


def object_from_name(name, module=None):
    parts = name.split('.')
    if module is None:
        parts_copy = parts[:]
        while parts_copy:
            try:
                module = __import__('.'.join(parts_copy))
                break
            except ImportError:
                del parts_copy[-1]
                if not parts_copy:
                    raise
        parts = parts[1:]

    parent = None
    obj = module
    for part in parts:
        parent, obj = obj, getattr(obj, part)
    return parent, obj



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


def isgenerator(obj):
    return (isgeneratorfunction(obj)
            or getattr(obj, 'testGenerator', None) is not None)


def safe_decode(string):
    if string is None:
        return string
    try:
        return string.decode()
    except UnicodeDecodeError:
        pass
    try:
        return string.decode('utf-8')
    except UnicodeDecodeError:
        return six.u('<unable to decode>')


def exc_info_to_string(err, test):
    formatTraceback = getattr(test, 'formatTraceback', None)
    if formatTraceback is not None:
        return test.formatTraceback(err)
    else:
        return format_traceback(test, err)


def format_traceback(test, err):
    """Converts a sys.exc_info()-style tuple of values into a string."""
    exctype, value, tb = err
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


def _is_relevant_tb_level(tb):
    return '__unittest' in tb.tb_frame.f_globals


def _count_relevant_tb_levels(tb):
    length = 0
    while tb and not _is_relevant_tb_level(tb):
        length += 1
        tb = tb.tb_next
    return length


class _WritelnDecorator(object):
    """Used to decorate file-like objects with a handy 'writeln' method"""
    def __init__(self, stream):
        self.stream = stream

    def __getattr__(self, attr):
        if attr in ('stream', '__getstate__'):
            raise AttributeError(attr)
        return getattr(self.stream, attr)

    def write(self, arg):
        self.stream.write(arg)

    def writeln(self, arg=None):
        if arg:
            self.stream.write(arg)
        self.stream.write('\n') # text-mode streams translate to \r\n if needed
