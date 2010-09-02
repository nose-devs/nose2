import inspect
from unittest2.plugins import moduleloading as ml


def unpack(_self, generator):
    for index, func_args in enumerate(generator):
        try:
            func, args = func_args
            if not isinstance(args, tuple):
                args = (args,)
            yield index, (func, args)
        except ValueError:
            func, args = func_args[0], func_args[1:]
            yield index, (func, args)


class Functions(ml.Functions):
    unpack = unpack

    def createTests(self, obj, testIndex=None):
        if not hasattr(obj, 'setUp'):
            if hasattr(obj, 'setup'):
                obj.setUp = obj.setup
            elif hasattr(obj, 'setUpFunc'):
                obj.setUp = obj.setUpFunc
        if not hasattr(obj, 'tearDown'):
            if hasattr(obj, 'teardown'):
                obj.tearDown = obj.teardowns
            elif hasattr(obj, 'tearDownFunc'):
                obj.tearDown = obj.tearDownFunc
        return super(Functions, self).createTests(obj, testIndex)

    def isGenerator(self, obj):
        return (inspect.isgeneratorfunction(obj) or
                super(Functions, self).isGenerator(obj))


class Generators(ml.Generators):
    unpack = unpack

    def isGenerator(self, obj):
        return (inspect.isgeneratorfunction(obj) or
                super(Generators, self).isGenerator(obj))



