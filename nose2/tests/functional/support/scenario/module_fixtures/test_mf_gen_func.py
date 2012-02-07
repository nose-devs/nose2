THINGS = []


def setUpModule():
   THINGS.append(1)


def tearDownModule():
    while THINGS:
        THINGS.pop()


def check(_):
   assert THINGS, "setup didn't run I think"


def test():
   yield check, 1
