myglob = 1


def test_w_global():
    global myglob
    assert myglob == 2
