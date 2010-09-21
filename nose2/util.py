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
