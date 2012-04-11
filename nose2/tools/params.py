"""
This module contains some code copied from unittest2 and other
code developed in reference to unittest2.

unittest2 is Copyright (c) 2001-2010 Python Software Foundation; All
Rights Reserved. See: http://docs.python.org/license.html

"""
__unittest = True


def params(*paramList):
    """Make a test function or method parameterized."""
    def decorator(func):
        func.paramList = paramList
        return func
    return decorator
