myglob = 1


def test_w_global():
    global myglob  # noqa: F824
    assert myglob == 2
