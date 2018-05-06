"""
Make assert statements print pretty output, including source.

This makes ``assert x == y`` more usable, as an alternative to
``self.assertEqual(x, y)``

This plugin implements :func:`outcomeDetail` and checks for event.exc_info
If it finds that an AssertionError happened, it will inspect the traceback and
add additional detail to the error report.

"""

from __future__ import print_function

import inspect
import re
import six
import textwrap
import tokenize

from nose2 import events


__unittest = True


class PrettyAssert(events.Plugin):
    """Add pretty output for "assert" statements"""
    configSection = 'pretty-assert'
    commandLineSwitch = (
        None, 'pretty-assert', 'Add pretty output for "assert" statements')

    def outcomeDetail(self, event):
        # skip if no exception or expected error
        if (not event.outcomeEvent.exc_info) or event.outcomeEvent.expected:
            return

        # unpack, but skip if it's not an AssertionError
        excty, exc, tb = event.outcomeEvent.exc_info
        if excty is not AssertionError:
            return

        self.addAssertDetail(event.extraDetail, exc, tb)

    @staticmethod
    def addAssertDetail(extraDetail, exc, tb):
        """
        Add details to output regarding AssertionError and its context
        """
        source_lines, f_locals, f_globals, statement = (
            _get_inspection_info(tb))

        # no message was given
        if len(exc.args) == 0:
            message = None
        else:
            message = exc.args[0]

        assert_startline, token_descriptions = _tokenize_assert(
            source_lines, f_locals, f_globals)

        #
        # actually add exception info to detail
        #

        # if we found an "assert" (we might not, if someone raises
        # AssertionError themselves), grab the whole assertion statement
        if assert_startline is not None:
            # dedented, no trailing newline, >>> prefix
            extraDetail.append(
                re.sub(
                    '^', '>>> ',
                    textwrap.dedent(
                        ''.join(source_lines[assert_startline:]
                                ).rstrip('\n')
                    ),
                    flags=re.MULTILINE
                )
            )
        # as a fallback, grab whatever we think the statement was
        # easily deceived by multiline expressions
        else:
            extraDetail.append('>>> {}'.format(statement))
        if message:
            extraDetail.append('\nmessage:')
            extraDetail.append('    {}'.format(message))

        if token_descriptions:
            extraDetail.append('\nvalues:')
            extraDetail.extend(token_descriptions)


def _get_inspection_info(tb):
    """
    Pick apart a traceback for the info we actually want to inspect from it
    - lines of source (truncated)
    - locals and globals from execution frame
    - statement which failed (which can be garbage -- don't trust it)
    """
    (frame, fname, lineno, funcname, context, ctx_index) = (
        inspect.getinnerframes(tb)[-1])
    source_lines, firstlineno = inspect.getsourcelines(frame)
    # truncate to the code in this frame
    # - remove test function definition line
    # - remove anything after current assert statement
    source_lines = source_lines[1:(lineno - firstlineno + 1)]

    # the assertion line without its indent -- it may or may not be
    # something useful, as multiline expressions mess this up easily
    statement = context[ctx_index].strip()

    return source_lines, frame.f_locals, frame.f_globals, statement


def _tokenize_assert(source_lines, f_locals, f_globals):
    """
    Given a set of lines of source ending in a failing assert, plus the frame
    locals and globals, tokenize source.

    Only look at tokens in the final assert statement
    Resolve all names to repr() of values

    Return
        The line on which the assert starts (relative to start of
        source_lines)

        A collection of token descriptions, name=val suitable for directly
        adding to output
    """
    # a collection of found, relevant tokens
    # ultimately, we want this to contain the values of tokens found in the
    # assert statement which failed
    collect_tokens = []
    # track which tokens we've seen to avoid duplicates if a name appears
    # twice, as in `assert x != x`
    seen_tokens = set()

    def process_tokens(toktype, tok, start, end, line):
        """
        A tokenization processor for tokenize.generate_tokens
        Skips certain token types, class names, etc

        When an identifiable/usable token is found, add it to
        collect_tokens
        (which we add to extraDetail later)

        When an "assert" statement is found, reset the token collection
        and return the start line (relative to the text being tokenized)
        """
        # skip non "NAME" tokens
        if toktype != tokenize.NAME:
            return

        # assert statement was reached, reset
        # return the start line (start = (startrow, startcol))
        if tok == 'assert':
            del collect_tokens[:]
            seen_tokens.clear()
            return start[0]

        # skip tokens we've seen
        if tok in seen_tokens:
            return
        # add it (so we don't try it again unless we hit a new assert and
        # reset
        seen_tokens.add(tok)

        # try to resolve to a value
        try:
            value = f_locals[tok]
        except KeyError:
            try:
                value = f_globals[tok]
            except KeyError:
                # unresolveable name -- short circuit
                return

        # okay, get repr() for a good string representation
        value = repr(value)
        # append in the form we want to print
        collect_tokens.append('    {} = {}'.format(tok, value))

    # tokenize.generate_tokens requires a file-like object, so we need to
    # convert source_lines to a StringIO to give it that interface
    filelike_context = six.StringIO(textwrap.dedent(''.join(source_lines)))

    # track the first line of the assert statement
    # when the assert is on oneline, we'll have it easily, but a multiline
    # statement like
    #   assert (x ==
    #           1)
    # will leave us holding the last line of the statement,
    # e.g. "       1)", which is not useful
    # so every time a new assert is found, we get a value back indicate
    # that it's the start line
    #
    #   assert True
    #   assert False
    # works fine, because we'll just hold the last value
    #
    #   assert True
    #   assert False
    #   assert True
    # also works because we truncated source_lines to remove the final
    # assert, which we didn't reach during execution
    assert_startline = None
    # tokenize and process each token
    for tokty, tok, start, end, tok_lineno in (
            tokenize.generate_tokens(filelike_context.readline)):
        ret = process_tokens(tokty, tok, start, end, tok_lineno)
        if ret:
            assert_startline = ret

    # adjust assert_startline by 1 to become a valid index into the
    # source_lines -- "line 1" means "index 0"
    if assert_startline:
        assert_startline -= 1

    return assert_startline, collect_tokens
