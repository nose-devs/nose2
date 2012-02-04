THINGS = []


def setUpModule():
   THINGS.append(1)


def tearDownModule():
    while THINGS:
        THINGS.pop()


def test():
    assert THINGS, "setup didn't run I think"
