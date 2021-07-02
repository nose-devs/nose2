from nose2.tools import such

with such.A("system") as it:

    @it.should("do something")
    def test():
        pass


it.createTests(globals())
