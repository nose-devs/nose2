def check(_):
    pass


def test():
    for i in range(0, 600):
        yield check, i
