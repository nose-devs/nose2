def labels(*labels):
    """
    To tag testcase or testclass
    Will use these tags to select or discard tests at runtime

    Usage::

        class MyTest(unittest.TestCase):
            @testlabel('quick')
            def test_foo(self):
                pass

        @testlabel('basic')
        class MyTest(unittest.TestCase):
            def test_foo(self):
                pass

            def test_bar(self):
                pass
    """
    def decorator(obj):
        obj.__testlabels__ = set(labels)
        return obj
    return decorator
