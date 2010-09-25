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
