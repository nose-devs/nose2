import os
import re
import sys

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


IDENT_RE = re.compile(r'^[_a-zA-Z]\w*$r', re.UNICODE)
VALID_MODULE_RE = re.compile(r'[_a-zA-Z]\w*\.py$', re.UNICODE)


def ln(label, char='-', width=70):
    """Draw a divider, with label in the middle.

    >>> ln('hello there')
    '---------------------------- hello there -----------------------------'

    Width and divider char may be specified. Defaults are 70 and '-'
    respectively.

    """
    label_len = len(label) + 2
    chunk = (width - label_len) / 2
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


def ispackage(path):
    """
    Is this path a package directory?

    """
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
