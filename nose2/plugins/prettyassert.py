"""
Make assert statements print pretty output, including source.

This makes ``assert x == y`` more usable, as an alternative to
``self.assertEqual(x, y)``

This plugin implements :func:`outcomeDetail` and checks for event.exc_info
If it finds that an AssertionError happened, it will inspect the traceback and
add additional detail to the error report.

"""

from __future__ import print_function

import collections
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

    token_processor = TokenProcessor(f_locals, f_globals)

    # tokenize and process each token
    for tokty, tok, start, end, tok_lineno in (
            tokenize.generate_tokens(filelike_context.readline)):
        ret = token_processor.process(tokty, tok, start, end, tok_lineno)
        if ret:
            assert_startline = ret

    # adjust assert_startline by 1 to become a valid index into the
    # source_lines -- "line 1" means "index 0"
    if assert_startline:
        assert_startline -= 1

    collect_tokens = []
    for (name, obj) in token_processor.get_token_collection().items():
        # okay, get repr() for a good string representation
        strvalue = repr(obj)
        # append in the form we want to print
        collect_tokens.append('    {} = {}'.format(name, strvalue))

    return assert_startline, collect_tokens


class TokenProcessor(object):
    def __init__(self, f_locals, f_globals):
        # local and global variables from the frame which we're inspecting
        self.f_locals, self.f_globals = f_locals, f_globals

        # None or a tuple of (object, name) where
        # - "object" is the object whose attributes we are currently resolving
        # - "name" is its name, as we would like to display it
        #
        # start each time we see a sequence of NAME OP NAME OP NAME (etc.)
        # end each time we see a token which is neither NAME nor OP
        self.doing_resolution = None

        # an index of known token names (including the long "x.y.z" names we
        # get from attribute resolution) to their values, in the order in which
        # they were encountered
        # track which tokens we've seen to avoid duplicates if a name appears
        # twice, as in `assert x != x`
        self.seen_tokens = collections.OrderedDict()

        # the previous token seen as a tuple of (tok_type, token_name)
        # (or None when we start)
        self.last_tok = None

    def get_token_collection(self):
        return self.seen_tokens

    def process(self, toktype, tok, start, end, line):
        """
        A tokenization processor for tokenize.generate_tokens
        Skips certain token types, class names, etc

        When an identifiable/usable token is found, add it to
        collect_tokens
        (which we add to extraDetail later)

        When an "assert" statement is found, reset the token collection
        and return the start line (relative to the text being tokenized)
        """
        prior_tok = self.last_tok
        self.last_tok = (toktype, tok)

        # CASE 0: skip non "NAME" or "OP" tokens and clear current resolution
        #
        # NAME is most identifiers and keywords
        # OP is operators, including .
        if toktype not in (tokenize.NAME, tokenize.OP):
            self.doing_resolution = None
            return

        """
        CASE 1: Operator token

        skip tokens and either leave resolution in progress or reset, depending

        continue resolution for
          "."
            because that's what attribute resolution *is*
          ")"
            this is handy, as it means that "(x).y" works

        reset resolution for everything else, e.g. "[", "]", ":"
        special note: reset resolution for "("

        failing to filter out ")" can result in badness in cases like this:
            >>> def foo():
            >>>     return [1]
            >>> foo.pop = 2
            >>> ...
            >>> def test_foo():
            >>>    assert foo().pop() == 2

        if we stop resolution when we see an LPAREN, we resolve `foo`
        successfully, fail on `pop` and everything is OK, but if we try to
        traverse the LPAREN, we get `foo.pop = 2` in our values, which is
        wrong
        """
        if toktype == tokenize.OP:
            if tok not in (".", ")"):
                self.doing_resolution = None
            return

        # CASE 2: "assert" statement
        # assert statement was reached, reset
        # return the start line (start = (startrow, startcol))
        if tok == 'assert':
            self.seen_tokens.clear()
            self.doing_resolution = None
            return start[0]

        # handle tokens

        # CASE 3: a name is being resolved,
        #         there is a previous token,
        #         and it's a "." operator
        if self.doing_resolution and prior_tok and (
                prior_tok[0] == tokenize.OP and prior_tok[1] == '.'):
            # unpack and look for the attribute
            obj, name = self.doing_resolution
            if hasattr(obj, tok):
                obj = getattr(obj, tok)
                name = name + '.' + tok
                self.doing_resolution = (obj, name)
                self.seen_tokens[name] = obj
            # if we couldn't find a relevant attribute, reset on resolution so
            # that we can try afresh
            else:
                self.doing_resolution = None

        # CASE 4: a name is being resolved and there is no preceding "." or
        #         resolution was explicitly stopped
        else:
            # skip tokens we've seen, but grab them as the current things under
            # resolution
            if tok in self.seen_tokens:
                self.doing_resolution = (self.seen_tokens[tok], tok)
                return
            # we've never seen this token before
            else:
                # try to resolve to a value
                try:
                    value = self.f_locals[tok]
                except KeyError:
                    try:
                        value = self.f_globals[tok]
                    except KeyError:
                        # unresolveable name -- short circuit
                        return

                # add it (so we don't try it again unless we hit a new assert
                # and reset)
                self.seen_tokens[tok] = value

                self.doing_resolution = (value, tok)
